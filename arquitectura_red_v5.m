%% =========================================================================
% TFG: Arquitectura Late Fusion MULTIMODAL - INTENTO #6 (Augmented + MGMT)
% =========================================================================
clear; clc; close all;

%% 1. CARGA Y PREPARACIÓN DE DATOS
disp('Cargando archivo maestro limpio y saneando datos...');
rutaCSV = 'C:\Users\Usuario\Documents\UAX\4º\TFG\DATOS\MAPA_MAESTRO_COMPLETO_2.csv';

% Importante: Guardamos el resultado directamente en la variable 'tabla'
tabla = readtable(rutaCSV, 'VariableNamingRule', 'preserve'); 

% 1.1. Conversión de la Clase Objetivo
% Forzamos la conversión usando el acceso estándar por cadena de texto
tabla.clase_respuesta = categorical(tabla.clase_respuesta);

% Identificamos las columnas de control y rutas para excluirlas del brazo clínico
rutasColumnas = {'Ruta_T1', 'Ruta_T1c', 'Ruta_T2', 'Ruta_FLAIR', 'Ruta_ADC', 'Ruta_ASL'};
columnasExcluidas = [rutasColumnas, {'ID', 'ID_Original', 'Set', 'clase_respuesta'}];

% Filtramos las columnas que no están en la lista de exclusión
esColumnaCandidata = ~ismember(tabla.Properties.VariableNames, columnasExcluidas);
nombresCandidatos = tabla.Properties.VariableNames(esColumnaCandidata);

% --- FILTRO: Solo nos quedamos con columnas de tipo numérico o lógico ---
esNumerica = false(1, length(nombresCandidatos));
for i = 1:length(nombresCandidatos)
    varNombre = nombresCandidatos{i};
    if isnumeric(tabla.(varNombre)) || islogical(tabla.(varNombre))
        esNumerica(i) = true;
    end
end
nombresClinicas = nombresCandidatos(esNumerica);

% 1.2. Construcción Segura de la Matriz de Características Tabulares
matrizClinica = table2array(tabla(:, nombresClinicas));
matrizClinica(isnan(matrizClinica)) = 0; 
tabla.MatrizFeatures = matrizClinica;

numFeatures = size(matrizClinica, 2);
fprintf('\n¡Saneamiento exitoso! Pasadas a la red %d características numéricas.\n', numFeatures);
disp('Variables incluidas en el brazo tabular:');
disp(nombresClinicas);

% 1.3. Filtro de Pacientes (Seguridad de Rutas)
filasValidas = true(height(tabla), 1);
for i = 1:length(rutasColumnas)
    colRuta = rutasColumnas{i};
    esError = strcmp(tabla.(colRuta), 'ARCHIVO_NO_ENCONTRADO') | strcmp(tabla.(colRuta), 'CARPETA_NO_EXISTE');
    filasValidas = filasValidas & ~esError;
end
tabla = tabla(filasValidas, :);
%% 2. BALANCEO Y DATASTORES
disp('Configurando Datastores con Data Augmentation...');
tablaTrain = tabla(strcmp(tabla.Set, 'Train'), :);
tablaVal   = tabla(strcmp(tabla.Set, 'Validation'), :);
tablaTest  = tabla(strcmp(tabla.Set, 'Test'), :);

% Oversampling previo para equilibrar el entrenamiento
filasClase2 = tablaTrain(tablaTrain.clase_respuesta == "2", :);
filasClase3 = tablaTrain(tablaTrain.clase_respuesta == "3", :);
tablaTrainBalanced = [tablaTrain; repmat(filasClase2, 2, 1); repmat(filasClase3, 3, 1)];
tablaTrainBalanced = tablaTrainBalanced(randperm(height(tablaTrainBalanced)), :);

% Activamos Data Augmentation exclusivamente para el set de Entrenamiento
doAugment = true;
dsTrain = helperCrearDatastore(tablaTrainBalanced, rutasColumnas, doAugment);
dsVal   = helperCrearDatastore(tablaVal, rutasColumnas, false);
dsTest  = helperCrearDatastore(tablaTest, rutasColumnas, false);

%% 3. ARQUITECTURA (V4 Optimizada con entrada adaptativa)
disp('Cargando arquitectura optimizada con dimensiones adaptadas...');
inputImage = image3dInputLayer([128 128 64 6], 'Name', 'input_img', 'Normalization', 'none');

branchImg = [ 
    convolution3dLayer(3, 16, 'Padding', 'same', 'Name', 'conv1')
    batchNormalizationLayer('Name', 'bn1')
    reluLayer('Name', 'relu1')
    maxPooling3dLayer(2, 'Stride', 2, 'Name', 'pool1')
    
    convolution3dLayer(3, 32, 'Padding', 'same', 'Name', 'conv2')
    batchNormalizationLayer('Name', 'bn2')
    reluLayer('Name', 'relu2')
    maxPooling3dLayer(2, 'Stride', 2, 'Name', 'pool2')
    
    convolution3dLayer(3, 64, 'Padding', 'same', 'Name', 'conv3')
    batchNormalizationLayer('Name', 'bn3')
    reluLayer('Name', 'relu3')
    
    globalAveragePooling3dLayer('Name', 'gap_img')
    flattenLayer('Name', 'flatten_gap')
    fullyConnectedLayer(64, 'Name', 'fc_img_final')
    dropoutLayer(0.4, 'Name', 'drop_img') 
];

% Adaptación dinámica al nuevo número de variables tabulares
inputTabular = featureInputLayer(numFeatures, 'Name', 'input_tab');
branchTab = [ 
    fullyConnectedLayer(64, 'Name', 'fc_tab1')
    reluLayer('Name', 'relu_tab1')
    fullyConnectedLayer(32, 'Name', 'fc_tab2')
    reluLayer('Name', 'relu_tab2')
];

nombresClases = categories(tabla.clase_respuesta);
pesosClases = [0.8, 1.2, 1.5]; % Pesos suavizados validados en V4

fusedLayers = [ 
    concatenationLayer(1, 2, 'Name', 'concat')
    fullyConnectedLayer(64, 'Name', 'fc_fusion')
    reluLayer('Name', 'relu_fusion')
    fullyConnectedLayer(3, 'Name', 'fc_final')
    softmaxLayer('Name', 'softmax')
    classificationLayer('Name', 'output', 'Classes', nombresClases, 'ClassWeights', pesosClases)
];

lgraph = layerGraph();
lgraph = addLayers(lgraph, inputImage);
lgraph = addLayers(lgraph, branchImg);
lgraph = addLayers(lgraph, inputTabular);
lgraph = addLayers(lgraph, branchTab);
lgraph = addLayers(lgraph, fusedLayers);

lgraph = connectLayers(lgraph, 'input_img', 'conv1');
lgraph = connectLayers(lgraph, 'input_tab', 'fc_tab1');
lgraph = connectLayers(lgraph, 'drop_img', 'concat/in1');
lgraph = connectLayers(lgraph, 'relu_tab2', 'concat/in2');

%% 4. ENTRENAMIENTO
options = trainingOptions('adam', ...
    'InitialLearnRate', 5e-4, ...
    'LearnRateSchedule', 'piecewise', ...
    'LearnRateDropFactor', 0.5, ...
    'LearnRateDropPeriod', 15, ...
    'MaxEpochs', 50, ... 
    'MiniBatchSize', 16, ...
    'ValidationData', dsVal, ...
    'Plots', 'training-progress', ...
    'Shuffle', 'every-epoch');

disp('Iniciando entrenamiento multimodal...');
net = trainNetwork(dsTrain, lgraph, options);

%% 5. EVALUACIÓN Y CURVAS ROC
disp('Generando métricas de evaluación y curvas ROC...');

% 5.1. Obtener probabilidades (scores)
scores = predict(net, dsTest);
[~, idxPred] = max(scores, [], 2);

% Forzamos que las predicciones sean del tipo categorical idéntico a clasesReales
predicciones = categorical(idxPred, 1:length(nombresClases), nombresClases);
clasesReales = tablaTest.clase_respuesta;

% 5.2. Matriz de Confusión
figure('Name', 'Matriz de Confusión');
plotconfusion(clasesReales, predicciones);

% 5.3. Curvas ROC por Clase
figure('Name', 'Curvas ROC por Clase', 'Color', 'w');
hold on;
colores = ['r', 'g', 'b']; 
for i = 1:length(nombresClases)
    probabilidadesClase = scores(:, i);
    claseObjetivo = nombresClases(i);
    
    [X, Y, T, AUC] = perfcurve(clasesReales, probabilidadesClase, char(claseObjetivo));
    
    plot(X, Y, 'Color', colores(i), 'LineWidth', 2, ...
        'DisplayName', ['Clase ' char(claseObjetivo) ' (AUC: ' num2str(AUC, '%.2f') ')']);
end
plot([0 1], [0 1], 'k--', 'HandleVisibility', 'off');
xlabel('1 - Especificidad');
ylabel('Sensibilidad');
title('Análisis ROC');
legend('Location', 'southeast');
grid on;
hold off;

%% =========================================================================
% FUNCIONES AUXILIARES PARA EL DATASTORE
% =========================================================================
function dsFinal = helperCrearDatastore(T, columnasRutas, doAugment)
    dsT1    = imageDatastore(T.(columnasRutas{1}), 'FileExtensions', {'.gz','.nii'}, 'ReadFcn', @niftiread);
    dsT1c   = imageDatastore(T.(columnasRutas{2}), 'FileExtensions', {'.gz','.nii'}, 'ReadFcn', @niftiread);
    dsT2    = imageDatastore(T.(columnasRutas{3}), 'FileExtensions', {'.gz','.nii'}, 'ReadFcn', @niftiread);
    dsFLAIR = imageDatastore(T.(columnasRutas{4}), 'FileExtensions', {'.gz','.nii'}, 'ReadFcn', @niftiread);
    dsADC   = imageDatastore(T.(columnasRutas{5}), 'FileExtensions', {'.gz','.nii'}, 'ReadFcn', @niftiread);
    dsASL   = imageDatastore(T.(columnasRutas{6}), 'FileExtensions', {'.gz','.nii'}, 'ReadFcn', @niftiread);
    
    dsCombinedImg = combine(dsT1, dsT1c, dsT2, dsFLAIR, dsADC, dsASL);
    
    if doAugment
        dsStackedImg = transform(dsCombinedImg, @(data) augmentAndStack(data));
    else
        dsStackedImg = transform(dsCombinedImg, @(data) cat(4, data{:}));
    end
    
    C = num2cell(T.MatrizFeatures, 2); 
    C = cellfun(@(x) x', C, 'UniformOutput', false); 
    dsClinico = transform(arrayDatastore(C, 'IterationDimension', 1), @(x) x{1});
    
    dsLabels = arrayDatastore(T.clase_respuesta, 'IterationDimension', 1);
    dsFinal = combine(dsStackedImg, dsClinico, dsLabels);
end

function out = augmentAndStack(data)
    vol = cat(4, data{:}); 
    if rand > 0.5
        vol = flip(vol, 2);
    end
    angle = (rand*4) - 2; 
    vol = imrotate(vol, angle, 'bilinear', 'crop');
    out = vol;
end