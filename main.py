import MyModule
import PySimpleGUI as sg

if __name__ == '__main__':

    sg.theme('DarkAmber')

    main_column = [
        [sg.Text('', key='positive_label_text')],
        [
            sg.Frame('Model 1', [
                [sg.Text('', key='model1_text1', visible=False)],
                [sg.Text('', key='model1_text2', visible=False)],
                [sg.Text('', key='model1_text3', visible=False)],
                [sg.Text('', key='model1_text4', visible=False)],
                [sg.Text('', key='model1_text5', visible=False)],
                [sg.Text('', key='model1_text6', visible=False)],
                [sg.Text('', key='model1_text7', visible=False)],
                [sg.Text('', key='model1_text8', visible=False)],
            ], key='frame_model1', size=(300, 250),
                     tooltip="Pogrubiona czcionka oznacza że wyróżniony wyznacznik jest lepszy"),
            sg.Frame('Model 2', [
                [sg.Text('', key='model2_text1', visible=False)],
                [sg.Text('', key='model2_text2', visible=False)],
                [sg.Text('', key='model2_text3', visible=False)],
                [sg.Text('', key='model2_text4', visible=False)],
                [sg.Text('', key='model2_text5', visible=False)],
                [sg.Text('', key='model2_text6', visible=False)],
                [sg.Text('', key='model2_text7', visible=False)],
                [sg.Text('', key='model2_text8', visible=False)],
            ], key='frame_model2', size=(300, 250),
                     tooltip="Pogrubiona czcionka oznacza że wyróżniony wyznacznik jest lepszy")
        ],
        [sg.Text('', key='graph_title_text', visible=True, justification='center', expand_x=True)],
        [sg.Graph((300, 250), (0, 0), (1, 1), float_values=True, background_color='white',
                  key='model1_graph'),
         sg.Graph((300, 250), (0, 0), (1, 1), float_values=True, background_color='white',
                  key='model2_graph')]
    ]

    layout = [[sg.FileBrowse('Wybierz plik CSV', file_types=(('Pliki CSV', '*.csv'),),
                             key='file_choice', enable_events=True)],
              [sg.Text('', key='file_info')],
              [sg.Combo(['Klasyfikacja', 'Regresja'], default_value='Klasyfikacja', key='model_choice',
                        readonly=True, enable_events=True)],
              [sg.Text('Indeksy (opcjonalne)', font='Any 10 underline',
                       tooltip="Indeksy interesujących kolumn jeśli plik zawiera więcej kolumn niż to założone\n"
                               "Indeksowanie rozpoczyna się od zera\n "
                               "Należy podawać wartości całkowite po przecinku, w odpowiedniej kolejności\n"
                               "Kolejność dla klasyfikacji:\n"
                               "0. Prawdziwe dane\n"
                               "1. Przewidywanie modelu 1\n"
                               "2. Prawdopodobieństwo klasy wyróżnionej w modelu 1\n"
                               "3. Przewidywanie modelu 2\n"
                               "4. Prawdopodobieństwo klasy wyróżnionej w modelu 1\n"
                               "Kolejność dla regresji:\n"
                               "0. Prawdziwe dane\n"
                               "1. Przewidywanie modelu 1\n"
                               "2. Przewidywanie modelu 2\n"
                               "Przykład: '1,2,3' lub '5, 6, 4, 3, 1'"), sg.InputText(key='indices')],
              [sg.Checkbox('Odwróć klasę pozytywną', key='positive_class', font='Any 10 underline',
                           tooltip="Zaznacz jeśli program zwraca ocenę modelu dla niewłaściwej klasy pozytywnej")],
              [sg.Button('Oceń', disabled=True, key='Calculate'), sg.Button('Cancel')],
              [sg.Column(main_column, visible=False, key='main_column')]]

    # Create the Window
    window = sg.Window('Zadanie Programistyczne 2', layout, location=(300, 100))

    data, header = [], None
    indices = None
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        elif event == 'file_choice':
            data, header = MyModule.read_csv(values['file_choice'])
            if len(data) > 0:
                window['file_info'].update("Wczytano: " + str(len(data)) + " rzędów " + str(len(data[0])) + " kolumn")
                window['Calculate'].update(disabled=False)
        elif event == 'model_choice':
            if values['model_choice'] == 'Klasyfikacja':
                window['positive_class'].update(disabled=False)
            else:
                window['positive_class'].update(disabled=True)
        elif event == 'Calculate':
            try:
                indices = values['indices']
                indices = tuple(map(int, indices.split(',')))
            except ValueError:
                pass
            if indices is None or len(indices) == 0:
                if values['model_choice'] == 'Klasyfikacja':
                    indices = (0, 1, 2, 3, 4)
                else:
                    indices = (0, 1, 2)

            if values['model_choice'] == "Klasyfikacja":
                prediction_data = MyModule.get_data_lists(data, (indices[0], indices[1], indices[3]))
                model_1_probability_data = MyModule.get_data_lists(data, (indices[0], indices[2]))
                model_2_probability_data = MyModule.get_data_lists(data, (indices[0], indices[4]))

                labels = MyModule.get_unique_values(prediction_data[0], max_len=2)
                if values['positive_class']:
                    tmp = labels[0]
                    labels[0] = labels[1]
                    labels[1] = tmp
                positive_label = labels[0]

                window['positive_label_text'].update("Klasa pozytywna: " + str(positive_label))
                model_1_ROC_points = MyModule.ROC_curve(model_1_probability_data, labels)
                model_2_ROC_points = MyModule.ROC_curve(model_2_probability_data, labels)
                model_1_auc = MyModule.calc_AUC(model_1_ROC_points)
                model_2_auc = MyModule.calc_AUC(model_2_ROC_points)

                model_1_confusion_matrix = MyModule.calculate_confusion_matrix(prediction_data, labels, indices=(0, 1))
                model_2_confusion_matrix = MyModule.calculate_confusion_matrix(prediction_data, labels, indices=(0, 2))

                model_1_quality_assessment = MyModule.classification_model_quality_assessment(model_1_confusion_matrix)
                model_2_quality_assessment = MyModule.classification_model_quality_assessment(model_2_confusion_matrix)

                window['model1_text1'].update("Trafność: " + str(round(model_1_quality_assessment['accuracy'], 2)),
                                              visible=True)
                window['model1_text2'].update(
                    "Całkowity współczynnik błędu: " + str(round(model_1_quality_assessment['overall_error_rate'], 2)),
                    visible=True)
                window['model1_text3'].update("Czułość: " + str(round(model_1_quality_assessment['sensitivity'], 2)),
                                              visible=True)
                window['model1_text4'].update(
                    "Wskaźnik fałszywie negatywnych: " + str(round(model_1_quality_assessment['fnr'], 2)), visible=True)
                window['model1_text5'].update(
                    "Specyficzność: " + str(round(model_1_quality_assessment['specificity'], 2)), visible=True)
                window['model1_text6'].update(
                    "Wskaźnik fałszywie pozytywnych: " + str(round(model_1_quality_assessment['fpr'], 2)), visible=True)
                window['model1_text7'].update("Precyzja: " + str(round(model_1_quality_assessment['precision'], 2)),
                                              visible=True)
                window['model1_text8'].update("Wynik F1: " + str(round(model_1_quality_assessment['f1'], 2)),
                                              visible=True)

                window['model2_text1'].update("Trafność: " + str(round(model_2_quality_assessment['accuracy'], 2)),
                                              visible=True)
                window['model2_text2'].update(
                    "Całkowity współczynnik błędu: " + str(round(model_2_quality_assessment['overall_error_rate'], 2)),
                    visible=True)
                window['model2_text3'].update("Czułość: " + str(round(model_2_quality_assessment['sensitivity'], 2)),
                                              visible=True)
                window['model2_text4'].update(
                    "Wskaźnik fałszywie negatywnych: " + str(round(model_2_quality_assessment['fnr'], 2)), visible=True)
                window['model2_text5'].update(
                    "Specyficzność: " + str(round(model_2_quality_assessment['specificity'], 2)), visible=True)
                window['model2_text6'].update(
                    "Wskaźnik fałszywie pozytywnych: " + str(round(model_2_quality_assessment['fpr'], 2)), visible=True)
                window['model2_text7'].update("Precyzja: " + str(round(model_2_quality_assessment['precision'], 2)),
                                              visible=True)
                window['model2_text8'].update("Wynik F1: " + str(round(model_2_quality_assessment['f1'], 2)),
                                              visible=True)

                if model_1_quality_assessment['accuracy'] > model_2_quality_assessment['accuracy']:
                    window['model1_text1'].update(font='Any 10 bold')
                    window['model2_text1'].update(font='Any 10 normal')
                else:
                    window['model2_text1'].update(font='Any 10 bold')
                    window['model1_text1'].update(font='Any 10 normal')

                if model_1_quality_assessment['overall_error_rate'] < model_2_quality_assessment['overall_error_rate']:
                    window['model1_text2'].update(font='Any 10 bold')
                    window['model2_text2'].update(font='Any 10 normal')
                else:
                    window['model2_text2'].update(font='Any 10 bold')
                    window['model1_text2'].update(font='Any 10 normal')

                if model_1_quality_assessment['sensitivity'] > model_2_quality_assessment['sensitivity']:
                    window['model1_text3'].update(font='Any 10 bold')
                    window['model2_text3'].update(font='Any 10 normal')
                else:
                    window['model2_text3'].update(font='Any 10 bold')
                    window['model1_text3'].update(font='Any 10 normal')

                if model_1_quality_assessment['fnr'] < model_2_quality_assessment['fnr']:
                    window['model1_text4'].update(font='Any 10 bold')
                    window['model2_text4'].update(font='Any 10 normal')
                else:
                    window['model2_text4'].update(font='Any 10 bold')
                    window['model1_text4'].update(font='Any 10 normal')

                if model_1_quality_assessment['specificity'] > model_2_quality_assessment['specificity']:
                    window['model1_text5'].update(font='Any 10 bold')
                    window['model2_text5'].update(font='Any 10 normal')
                else:
                    window['model2_text5'].update(font='Any 10 bold')
                    window['model1_text5'].update(font='Any 10 normal')

                if model_1_quality_assessment['fpr'] < model_2_quality_assessment['fpr']:
                    window['model1_text6'].update(font='Any 10 bold')
                    window['model2_text6'].update(font='Any 10 normal')
                else:
                    window['model2_text6'].update(font='Any 10 bold')
                    window['model1_text6'].update(font='Any 10 normal')

                if model_1_quality_assessment['precision'] > model_2_quality_assessment['precision']:
                    window['model1_text7'].update(font='Any 10 bold')
                    window['model2_text7'].update(font='Any 10 normal')
                else:
                    window['model2_text7'].update(font='Any 10 bold')
                    window['model1_text7'].update(font='Any 10 normal')

                if model_1_quality_assessment['f1'] > model_2_quality_assessment['f1']:
                    window['model1_text8'].update(font='Any 10 bold')
                    window['model2_text8'].update(font='Any 10 normal')
                else:
                    window['model2_text8'].update(font='Any 10 bold')
                    window['model1_text8'].update(font='Any 10 normal')

                window['graph_title_text'].update("Krzywe ROC")

                window['model1_graph'].erase()
                window['model1_graph'].draw_line((0, 0), (1, 1), 'blue', 1)
                for i in range(0, 10, 2):
                    window['model1_graph'].draw_line((i / 10, 0), (i / 10, 1), 'gray', 1)
                    window['model1_graph'].draw_line((0, i / 10), (1, i / 10), 'gray', 1)
                    window['model1_graph'].draw_text(str(i / 10), (i / 10, 0.05), 'black')
                    window['model1_graph'].draw_text(str(i / 10), (0.05, i / 10), 'black')
                for i in range(len(model_1_ROC_points) - 1):
                    window['model1_graph'].draw_line(model_1_ROC_points[i], model_1_ROC_points[i + 1], 'red', 2)
                window['model1_graph'].draw_rectangle((0.75, 0.25), (0.95, 0.15), 'lightgray')
                window['model1_graph'].draw_text("AUC= " + str(round(model_1_auc, 2)), (0.85, 0.2), 'black')

                window['model2_graph'].erase()
                window['model2_graph'].draw_line((0, 0), (1, 1), 'blue', 1)
                for i in range(0, 10, 2):
                    window['model2_graph'].draw_line((i / 10, 0), (i / 10, 1), 'gray', 1)
                    window['model2_graph'].draw_line((0, i / 10), (1, i / 10), 'gray', 1)
                    window['model2_graph'].draw_text(str(i / 10), (i / 10, 0.05), 'black')
                    window['model2_graph'].draw_text(str(i / 10), (0.05, i / 10), 'black')
                for i in range(len(model_2_ROC_points) - 1):
                    window['model2_graph'].draw_line(model_2_ROC_points[i], model_2_ROC_points[i + 1], 'red', 2)
                window['model2_graph'].draw_rectangle((0.75, 0.25), (0.95, 0.15), 'lightgray')
                window['model2_graph'].draw_text("AUC= " + str(round(model_2_auc, 2)), (0.85, 0.2), 'black')

            else:
                data = MyModule.get_data_lists(data, (indices[0], indices[1], indices[2]))
                data = [list(map(float, x)) for x in data]
                for i in range(len(data)):
                    data[i] = data[i][87:]
                model_1_quality_assessment, model_1_error_list = \
                    MyModule.regression_model_quality_assessment(list(zip(data[0], data[1])))
                model_2_quality_assessment, model_2_error_list = \
                    MyModule.regression_model_quality_assessment(list(zip(data[0], data[2])))

                window['model1_text1'].update("MAE: " + str(round(model_1_quality_assessment['mae'], 3)), visible=True)
                window['model1_text2'].update("MSE: " + str(round(model_1_quality_assessment['mse'], 3)), visible=True)
                window['model1_text3'].update("RMSE: " + str(round(model_1_quality_assessment['rmse'], 3)),
                                              visible=True)
                window['model1_text4'].update("MAPE: " + str(round(model_1_quality_assessment['mape'], 3)) + "%",
                                              visible=True)
                window['model1_text5'].update("", visible=True)
                window['model1_text6'].update("", visible=True)
                window['model1_text7'].update("", visible=True)
                window['model1_text8'].update("", visible=True)

                window['model2_text1'].update("MAE: " + str(round(model_2_quality_assessment['mae'], 3)), visible=True)
                window['model2_text2'].update("MSE: " + str(round(model_2_quality_assessment['mse'], 3)), visible=True)
                window['model2_text3'].update("RMSE: " + str(round(model_2_quality_assessment['rmse'], 3)),
                                              visible=True)
                window['model2_text4'].update("MAPE: " + str(round(model_2_quality_assessment['mape'], 3)) + "%",
                                              visible=True)
                window['model2_text5'].update("", visible=True)
                window['model2_text6'].update("", visible=True)
                window['model2_text7'].update("", visible=True)
                window['model2_text8'].update("", visible=True)

                window['positive_label_text'].update("", visible=True)

                if model_1_quality_assessment['mae'] < model_2_quality_assessment['mae']:
                    window['model1_text1'].update(font='Any 10 bold')
                    window['model2_text1'].update(font='Any 10 normal')
                else:
                    window['model2_text1'].update(font='Any 10 bold')
                    window['model1_text1'].update(font='Any 10 normal')

                if model_1_quality_assessment['mse'] < model_2_quality_assessment['mse']:
                    window['model1_text2'].update(font='Any 10 bold')
                    window['model2_text2'].update(font='Any 10 normal')
                else:
                    window['model2_text2'].update(font='Any 10 bold')
                    window['model1_text2'].update(font='Any 10 normal')

                if model_1_quality_assessment['rmse'] < model_2_quality_assessment['rmse']:
                    window['model1_text3'].update(font='Any 10 bold')
                    window['model2_text3'].update(font='Any 10 normal')
                else:
                    window['model2_text3'].update(font='Any 10 bold')
                    window['model1_text3'].update(font='Any 10 normal')

                if model_1_quality_assessment['mape'] < model_2_quality_assessment['mape']:
                    window['model1_text4'].update(font='Any 10 bold')
                    window['model2_text4'].update(font='Any 10 normal')
                else:
                    window['model2_text4'].update(font='Any 10 bold')
                    window['model1_text4'].update(font='Any 10 normal')

                model_1_histogram = MyModule.calc_histogram(model_1_error_list, 20)
                model_2_histogram = MyModule.calc_histogram(model_2_error_list, 20)

                model_1_histogram = [float(i) / max(model_1_histogram) for i in model_1_histogram]
                model_2_histogram = [float(i) / max(model_2_histogram) for i in model_2_histogram]

                normal_curve = [(0, 0), (0.05, 0.001463), (0.1, 0.005853), (0.15, 0.019268),
                                (0.2, 0.054634), (0.25, 0.131707), (0.3, 0.270487), (0.35, 0.473658),
                                (0.4, 0.706585), (0.45, 0.898292),
                                (0.4625, 0.930243), (0.475, 0.953658), (0.4875, 0.968292),
                                (0.5, 0.972926),
                                (0.5125, 0.968292), (0.525, 0.953658), (0.5375, 0.930243), (0.55, 0.898292),
                                (0.6, 0.706585), (0.65, 0.473658), (0.7, 0.270487), (0.75, 0.131707),
                                (0.8, 0.054634), (0.85, 0.019268), (0.9, 0.005853), (0.95, 0.001463),
                                (1.0, 0)
                                ]

                window['graph_title_text'].update("Histogramy różnic między wartościami")

                window['model1_graph'].erase()
                for val, i in zip(model_1_histogram, range(len(model_1_histogram))):
                    window['model1_graph'].draw_rectangle((i * 0.05, val), ((i + 1) * 0.05, 0), 'lightblue', 'black', 1)
                for i in range(0, 10, 2):
                    window['model1_graph'].draw_line((i / 10, 0), (i / 10, 1), 'gray', 1)
                    window['model1_graph'].draw_line((0, i / 10), (1, i / 10), 'gray', 1)
                    window['model1_graph'].draw_text(str(i / 10), (i / 10, 0.05), 'black')
                    window['model1_graph'].draw_text(str(i / 10), (0.05, i / 10), 'black')

                window['model2_graph'].erase()
                for val, i in zip(model_2_histogram, range(len(model_2_histogram))):
                    window['model2_graph'].draw_rectangle((i * 0.05, val), ((i + 1) * 0.05, 0), 'lightblue', 'black', 1)
                for i in range(0, 10, 2):
                    window['model2_graph'].draw_line((i / 10, 0), (i / 10, 1), 'gray', 1)
                    window['model2_graph'].draw_line((0, i / 10), (1, i / 10), 'gray', 1)
                    window['model2_graph'].draw_text(str(i / 10), (i / 10, 0.05), 'black')
                    window['model2_graph'].draw_text(str(i / 10), (0.05, i / 10), 'black')

                for i in range(len(normal_curve) - 1):
                    window['model1_graph'].draw_line(normal_curve[i], normal_curve[i+1], 'red', 1)
                    window['model2_graph'].draw_line(normal_curve[i], normal_curve[i+1], 'red', 1)

            window['main_column'].update(visible=True)
    window.close()

    # data, header = MyModule.read_csv('klasyfikacja_przykład.csv')
    # data, header = MyModule.read_csv('regresja_przykład.csv')
    # data, header = MyModule.read_csv('example.csv')

    # data = MyModule.get_data_lists(data, (8, 9, 10))
    # data = [list(map(float, x)) for x in data]
    # for i in range(len(data)):
    #     data[i] = data[i][87:]
    # model_1_quality_assessment, model_1_error_list = \
    #     MyModule.regression_model_quality_assessment(list(zip(data[0], data[1])))
    # model_2_quality_assessment, model_2_error_list = \
    #     MyModule.regression_model_quality_assessment(list(zip(data[0], data[2])))
    #
    # print(model_1_quality_assessment)
    # print(model_2_quality_assessment)

#     prediction_data = MyModule.get_data_lists(data, (0, 1, 3))
#     model_1_probability_data = MyModule.get_data_lists(data, (0, 2))
#     model_2_probability_data = MyModule.get_data_lists(data, (0, 4))
#
#     labels = MyModule.get_unique_values(prediction_data[0], max_len=2)
#     tmp = labels[0]
#     labels[0] = labels[1]
#     labels[1] = tmp
#     positive_label = labels[0]
#
#     # # start_time = time.time()
#     model_1_ROC_points = MyModule.ROC_curve(model_1_probability_data, labels)
#     # # print("Time1: ", time.time() - start_time)
#     # # start_time = time.time()
#     # model_2_ROC_points = MyModule.ROC_curve(model_2_probability_data, labels)
#     # # print("Time2: ", time.time() - start_time)
#
#     model_1_confusion_matrix = MyModule.calculate_confusion_matrix(prediction_data, labels, indices=(0, 1))
#     model_2_confusion_matrix = MyModule.calculate_confusion_matrix(prediction_data, labels, indices=(0, 2))
# #
#     model_1_quality_assessment = MyModule.classification_model_quality_assessment(model_1_confusion_matrix)
#     model_2_quality_assessment = MyModule.classification_model_quality_assessment(model_2_confusion_matrix)
#
#     auc = MyModule.calc_AUC(model_1_ROC_points)
#     print(auc)
#
#     for point in model_1_ROC_points:
#         print(point)
