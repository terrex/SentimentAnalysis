import QtQuick 2.2
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.3
import QtQuick.Window 2.2
import QtQuick.Dialogs 1.2

ApplicationWindow {
    id: rootWindow
    objectName: "rootWindow"
    width: 720
    height: 560
    minimumWidth: 720
    minimumHeight: 560

    menuBar: MenuBar {
        Menu {
            title: "File"
            MenuItem {
                text: qsTr("New")
                shortcut: StandardKey.New
            }
            MenuItem {
                text: qsTr("Open...")
                shortcut: StandardKey.Open
            }
            MenuItem {
                text: qsTr("Save...")
                shortcut: StandardKey.Save
            }
            MenuSeparator {
            }
            MenuItem {
                text: qsTr("Close")
                shortcut: StandardKey.Close
                onTriggered: rootWindow.close()
            }
        }

        Menu {
            title: "Edit"
            MenuItem {
                text: qsTr("Undo")
                shortcut: StandardKey.Undo
            }
            MenuItem {
                text: qsTr("Redo")
                shortcut: StandardKey.Redo
            }
            MenuSeparator {
            }
            MenuItem {
                text: qsTr("Cut")
                shortcut: StandardKey.Cut
            }
            MenuItem {
                text: qsTr("Copy")
                shortcut: StandardKey.Copy
            }
            MenuItem {
                text: qsTr("Paste")
                shortcut: StandardKey.Paste
            }
            MenuItem {
                text: qsTr("Select All")
                shortcut: StandardKey.SelectAll
            }
        }
    }

    FileDialog {
        id: fileDialogChooseTSV
        objectName: "fileDialogChooseTSV"
        nameFilters: ["Tab-separated files (*.tsv)"]
        onAccepted: {
            mainPfcsamrApp.findChild('load_train_file').text = fileUrl
            mainPfcsamrApp.findChild('load_button_load').enabled = true
        }
    }

    statusBar: StatusBar {
        RowLayout {
            Label {
                id: status_bar_label
                objectName: "status_bar_label"
                text: "Done"
            }
        }
    }

    SplitView {
        id: main_split_view
        objectName: 'main_split_view'
        anchors.fill: parent
        orientation: Qt.Vertical

        Rectangle {
            id: upper_split_view
            objectName: 'upper_split_view'
            Layout.minimumHeight: 300

            TabView {
                id: upper_tab_view
                objectName: 'upper_tab_view'
                anchors.fill: parent

                Tab {
                    id: load_tab
                    objectName: "load_tab"
                    title: "Load"
                    anchors.margins: 10

                    ColumnLayout {
                        RowLayout {
                            Button {
                                text: "Select file"
                                onClicked: fileDialogChooseTSV.open()
                            }
                            TextEdit {
                                id: load_train_file
                                objectName: "load_train_file"
                                text: mainPfcsamrApp.get_config_prop(
                                          'load_train_file')
                                Layout.fillWidth: true
                                readOnly: true
                                onTextChanged: mainPfcsamrApp.set_config_prop_value(
                                                   'load_train_file', text)
                            }
                        }
                        RowLayout {
                            CheckBox {
                                id: load_only_first
                                objectName: 'load_only_first'
                                text: "Load only first"
                                checked: mainPfcsamrApp.get_config_prop(
                                             'load_only_first')
                                onCheckedChanged: mainPfcsamrApp.set_config_prop_value(
                                                      'load_only_first',
                                                      checked)
                            }
                            SpinBox {
                                id: load_only_first_rows
                                objectName: 'load_only_first_rows'
                                enabled: load_only_first.checked
                                minimumValue: 0
                                maximumValue: 99999999 //Actualizar por código
                                value: mainPfcsamrApp.get_config_prop(
                                           'load_only_first_rows')
                                onValueChanged: mainPfcsamrApp.set_config_prop_value(
                                                    'load_only_first_rows',
                                                    value)
                            }
                            Label {
                                text: "samples"
                            }
                        }
                        RowLayout {
                            Button {
                                id: load_button_load
                                objectName: 'load_button_load'
                                text: "LOAD"
                                onClicked: mainPfcsamrApp.load_button_load_on_clicked()
                                enabled: false
                            }
                        }
                        RowLayout {
                            anchors.fill: parent
                        }
                    }
                }

                Tab {
                    id: preproc_tab
                    objectName: "preproc_tab"
                    title: "Preprocess"
                    anchors.margins: 10
                    ColumnLayout {
                        CheckBox {
                            id: preproc_unsplit_contractions
                            objectName: 'preproc_unsplit_contractions'
                            text: "unsplit contractions"
                            checked: mainPfcsamrApp.get_config_prop(
                                         'preproc_unsplit_contractions')
                            onCheckedChanged: mainPfcsamrApp.set_config_prop_value(
                                                  'preproc_unsplit_contractions',
                                                  checked)
                        }
                        CheckBox {
                            id: preproc_expand_contractions
                            objectName: 'preproc_expand_contractions'
                            anchors.left: parent.left
                            anchors.leftMargin: 10
                            text: "expand contractions"
                            enabled: preproc_unsplit_contractions.checked
                            onEnabledChanged: {
                                if (!enabled) {
                                    checked = false
                                }
                            }
                            checked: mainPfcsamrApp.get_config_prop(
                                         'preproc_expand_contractions')
                            onCheckedChanged: mainPfcsamrApp.set_config_prop_value(
                                                  'preproc_expand_contractions',
                                                  checked)
                        }
                        CheckBox {
                            id: preproc_remove_stopwords
                            objectName: 'preproc_remove_stopwords'
                            text: "remove stopwords"
                            checked: mainPfcsamrApp.get_config_prop(
                                         'preproc_remove_stopwords')
                            onCheckedChanged: mainPfcsamrApp.set_config_prop_value(
                                                  'preproc_remove_stopwords',
                                                  checked)
                        }
                        GroupBox {
                            id: preproc_word_replacement
                            objectName: 'preproc_word_replacement'
                            checkable: true
                            title: "word replacement"
                            checked: mainPfcsamrApp.get_config_prop(
                                         'preproc_word_replacement')
                            onCheckableChanged: mainPfcsamrApp.set_config_prop_value(
                                                    'preproc_word_replacement',
                                                    checked)
                            ExclusiveGroup {
                                id: stemmizeLemmatizeExclusiveGroup
                            }
                            ColumnLayout {
                                RadioButton {
                                    id: preproc_stemmize
                                    objectName: 'preproc_stemmize'
                                    text: "stemmize"
                                    exclusiveGroup: stemmizeLemmatizeExclusiveGroup
                                    checked: mainPfcsamrApp.get_config_prop(
                                                 'preproc_stemmize')
                                    onCheckedChanged: mainPfcsamrApp.set_config_prop_value(
                                                          'preproc_stemmize',
                                                          checked)
                                }
                                RadioButton {
                                    id: preproc_lemmatize
                                    objectName: 'preproc_lemmatize'
                                    text: "lemmatize"
                                    exclusiveGroup: stemmizeLemmatizeExclusiveGroup
                                    checked: mainPfcsamrApp.get_config_prop(
                                                 'preproc_lemmatize')
                                    onCheckedChanged: mainPfcsamrApp.set_config_prop_value(
                                                          'preproc_lemmatize',
                                                          checked)
                                }
                            }
                        }
                        CheckBox {
                            id: preproc_pos_tag_words
                            objectName: 'preproc_pos_tag_words'
                            text: "POS tag words"
                            checked: mainPfcsamrApp.get_config_prop(
                                         'preproc_pos_tag_words')
                            onCheckedChanged: mainPfcsamrApp.set_config_prop_value(
                                                  'preproc_pos_tag_words',
                                                  checked)
                        }
                        Button {
                            id: preproc_button_run
                            objectName: 'preproc_button_run'
                            text: "RUN"
                            onClicked: mainPfcsamrApp.preproc_button_run_on_clicked()
                        }

                        RowLayout {
                            anchors.fill: parent
                        }
                    }
                }

                Tab {
                    id: features_tab
                    objectName: "features_tab"
                    title: "Features"
                    anchors.margins: 10
                    ColumnLayout {
                        RowLayout {
                            CheckBox {
                                id: features_ngrams
                                objectName: 'features_ngrams'
                                text: "n-grams from"
                                checked: mainPfcsamrApp.get_config_prop(
                                             'features_ngrams')
                                onCheckedChanged: mainPfcsamrApp.set_config_prop_value(
                                                      'features_ngrams',
                                                      checked)
                            }
                            SpinBox {
                                id: features_ngrams_from
                                objectName: 'features_ngrams_from'
                                minimumValue: 1
                                maximumValue: Math.min(20,
                                                       features_ngrams_to.value)
                                enabled: features_ngrams.checked
                                value: mainPfcsamrApp.get_config_prop(
                                           'features_ngrams_from')
                                onValueChanged: mainPfcsamrApp.set_config_prop_value(
                                                    'features_ngrams_from',
                                                    value)
                            }
                            Label {
                                text: "to"
                                enabled: features_ngrams.checked
                            }
                            SpinBox {
                                id: features_ngrams_to
                                objectName: 'features_ngrams_to'
                                minimumValue: Math.max(
                                                  1, features_ngrams_from.value)
                                maximumValue: 20
                                value: mainPfcsamrApp.get_config_prop(
                                           'features_ngrams_to')
                                onValueChanged: mainPfcsamrApp.set_config_prop_value(
                                                    'features_ngrams_to', value)
                                enabled: features_ngrams.checked
                            }
                        }
                        RowLayout {
                            anchors.left: parent.left
                            anchors.leftMargin: 10
                            Label {
                                text: "with document frecuency contraints:"
                                enabled: features_ngrams.checked
                            }
                        }
                        RowLayout {
                            anchors.left: parent.left
                            anchors.leftMargin: 20
                            CheckBox {
                                id: features_minimum_df
                                objectName: 'features_minimum_df'
                                text: "a minimum of"
                                enabled: features_ngrams.checked
                                checked: mainPfcsamrApp.get_config_prop(
                                             'features_minimum_df')
                                onCheckedChanged: mainPfcsamrApp.set_config_prop_value(
                                                      'features_minimum_df',
                                                      checked)
                                onEnabledChanged: if (!enabled)
                                                      checked = false
                            }
                            SpinBox {
                                id: features_minimum_df_value
                                objectName: 'features_minimum_df_value'
                                minimumValue: 1
                                maximumValue: 99999999
                                enabled: features_minimum_df.checked
                                value: mainPfcsamrApp.get_config_prop(
                                           'features_minimum_df_value')
                                onValueChanged: mainPfcsamrApp.set_config_prop_value(
                                                    'features_minimum_df_value',
                                                    value)
                            }
                            ComboBox {
                                model: ["no. of documents", "% of documents"]
                                enabled: features_minimum_df.checked
                                currentIndex: mainPfcsamrApp.get_config_prop(
                                                  'features_minimum_df_unit')
                                onCurrentIndexChanged: mainPfcsamrApp.set_config_prop_value(
                                                           'features_minimum_df_unit',
                                                           currentIndex)
                            }
                        }
                        RowLayout {
                            anchors.left: parent.left
                            anchors.leftMargin: 20
                            CheckBox {
                                id: features_maximum_df
                                objectName: 'features_maximum_df'
                                text: "a maximum of"
                                enabled: features_ngrams.checked
                                onEnabledChanged: if (!enabled)
                                                      checked = false
                                checked: mainPfcsamrApp.get_config_prop(
                                             'features_maximum_df')
                                onCheckedChanged: mainPfcsamrApp.set_config_prop_value(
                                                      'features_maximum_df',
                                                      checked)
                            }
                            SpinBox {
                                id: features_maximum_df_value
                                objectName: 'features_maximum_df_value'
                                minimumValue: 1
                                maximumValue: 99999999
                                enabled: features_maximum_df.checked
                                value: mainPfcsamrApp.get_config_prop(
                                           'features_maximum_df_value')
                                onValueChanged: mainPfcsamrApp.set_config_prop_value(
                                                    'features_maximum_df_value',
                                                    value)
                            }
                            ComboBox {
                                id: features_maximum_df_unit
                                objectName: 'features_maximum_df_unit'
                                model: ["no. of documents", "% of documents"]
                                enabled: features_maximum_df.checked
                                currentIndex: mainPfcsamrApp.get_config_prop(
                                                  'features_maximum_df_unit')
                                onCurrentIndexChanged: mainPfcsamrApp.set_config_prop_value(
                                                           'features_maximum_df_unit',
                                                           currentIndex)
                            }
                        }
                        RowLayout {
                            anchors.left: parent.left
                            anchors.leftMargin: 10
                            CheckBox {
                                id: features_only_most_significant
                                objectName: 'features_only_most_significant'
                                text: "only most significant"
                                enabled: features_ngrams.checked
                                onEnabledChanged: if (!enabled)
                                                      checked = false
                                checked: mainPfcsamrApp.get_config_prop(
                                             'features_only_most_significant')
                                onCheckedChanged: mainPfcsamrApp.set_config_prop_value(
                                                      'features_only_most_significant',
                                                      checked)
                            }
                            SpinBox {
                                id: features_only_most_significant_feats
                                objectName: 'features_only_most_significant_feats'
                                minimumValue: 1
                                maximumValue: 1000
                                enabled: features_only_most_significant.checked
                                value: mainPfcsamrApp.get_config_prop(
                                           'features_only_most_significant_feats')
                                onValueChanged: mainPfcsamrApp.set_config_prop_value(
                                                    'features_only_most_significant_feats',
                                                    value)
                            }
                            Label {
                                text: "features"
                                enabled: features_only_most_significant.checked
                            }
                        }
                        RowLayout {
                            CheckBox {
                                id: features_remove_less_than
                                objectName: 'features_remove_less_than'
                                text: "remove features with less than"
                                checked: mainPfcsamrApp.get_config_prop(
                                             'features_remove_less_than')
                                onCheckedChanged: mainPfcsamrApp.set_config_prop_value(
                                                      'features_remove_less_than',
                                                      checked)
                            }
                            SpinBox {
                                id: features_remove_less_than_variance
                                objectName: 'features_remove_less_than_variance'
                                decimals: 2
                                stepSize: 0.01
                                minimumValue: 0
                                maximumValue: 99999999
                                enabled: features_remove_less_than.checked
                                value: mainPfcsamrApp.get_config_prop(
                                           'features_remove_less_than_variance')
                                onValueChanged: mainPfcsamrApp.set_config_prop_value(
                                                    'features_remove_less_than_variance',
                                                    value)
                            }
                            Label {
                                text: "variance"
                                enabled: features_remove_less_than.checked
                            }
                        }
                        RowLayout {
                            Button {
                                id: features_button_run
                                objectName: 'features_button_run'
                                text: "RUN"
                                onClicked: mainPfcsamrApp.features_button_run_on_clicked()
                            }
                            Button {
                                text: "Show selected features"
                            }
                        }

                        RowLayout {
                            anchors.fill: parent
                        }
                    }
                }

                Tab {
                    id: learn_tab
                    objectName: "learn_tab"
                    title: "Learn"
                    anchors.margins: 10
                    ColumnLayout {
                        RowLayout {
                            id: splitRandomlyRowLayout
                            CheckBox {
                                id: splitRandomly
                                text: "split randomly"
                            }
                            SpinBox {
                                minimumValue: 1
                                maximumValue: 99
                                suffix: " %"
                                enabled: splitRandomly.checked
                            }
                            Label {
                                text: "dataset for train and remaining for self-test"
                            }
                        }

                        RowLayout {
                            height: parent.height - splitRandomlyRowLayout.height - learnRUN.height
                            TabView {
                                anchors.fill: parent
                                Layout.fillWidth: true
                                Layout.fillHeight: true

                                Tab {
                                    title: "MultinomialNB"
                                }
                                Tab {
                                    title: "GaussianNB"
                                }
                                Tab {
                                    title: "LDA"
                                }
                                Tab {
                                    title: "QDA"
                                }
                                Tab {
                                    title: "LinearSVM"
                                }
                            }
                        }

                        Button {
                            id: learnRUN
                            text: "RUN"
                        }
                    }
                }

                Tab {
                    id: classify_tab
                    objectName: "classify_tab"
                    title: "Classify"
                    anchors.margins: 10
                    ColumnLayout {
                        //Aqui van los demás
                        RowLayout {
                            anchors.fill: parent
                        }
                    }
                }

                Tab {
                    id: test_tab
                    objectName: "test_tab"
                    title: "Test"
                    anchors.margins: 10
                    ColumnLayout {
                        //Aqui van los demás
                        RowLayout {
                            anchors.fill: parent
                        }
                    }
                }

                Tab {
                    id: evaluate_tab
                    objectName: "evaluate_tab"
                    title: "Evaluate"
                    anchors.margins: 10
                    ColumnLayout {
                        //Aqui van los demás
                        RowLayout {
                            anchors.fill: parent
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.minimumHeight: 100

            TableView {
                id: data_table_view
                objectName: 'data_table_view'
                anchors.fill: parent

                onModelChanged: {
                    while (columnCount > 0) {
                        removeColumn(0)
                    }
                    var table_headings = mainPfcsamrApp.get_table_headings()
                    for (var j = 0; j < table_headings.length; j++) {
                        addColumn(Qt.createQmlObject(
                                      'import QtQuick 2.2; import QtQuick.Controls 1.3; import QtQuick.Layouts 1.1;'
                                      + 'TableViewColumn{role:"' + table_headings[j]
                                      + '";title:"' + table_headings[j] + '";width:100;}',
                                      data_table_view))
                    }
                }
                itemDelegate: Item {
                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.fill: parent
                        color: styleData.textColor
                        elide: Text.ElideRight
                        text: mainPfcsamrApp.get_current_model_cell(
                                  styleData.row, styleData.column)
                    }
                }
            }
        }
    }
}
