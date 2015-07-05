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
                onTriggered: txtProgram.undo()
            }
            MenuItem {
                text: qsTr("Redo")
                shortcut: StandardKey.Redo
                onTriggered: txtProgram.redo()
            }
            MenuSeparator {
            }
            MenuItem {
                text: qsTr("Cut")
                shortcut: StandardKey.Cut
                onTriggered: txtProgram.cut()
            }
            MenuItem {
                text: qsTr("Copy")
                shortcut: StandardKey.Copy
                onTriggered: txtProgram.copy()
            }
            MenuItem {
                text: qsTr("Paste")
                shortcut: StandardKey.Paste
                onTriggered: txtProgram.paste()
            }
            MenuItem {
                text: qsTr("Select All")
                shortcut: StandardKey.SelectAll
                onTriggered: txtProgram.selectAll()
            }
        }
    }

    FileDialog {
        id: fileDialogChooseTSV
        objectName: "fileDialogChooseTSV"
        nameFilters: ["Tab-separated files (*.tsv)"]
        onAccepted: mainPfcsamrApp.findChild('load_train_file').text = fileUrl
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
                    id: loadTab
                    objectName: "loadTab"
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
                            }
                        }
                        RowLayout {
                            anchors.fill: parent
                        }
                    }
                }

                Tab {
                    id: preprocessTab
                    objectName: "preprocessTab"
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
                            text: "RUN"
                        }

                        RowLayout {
                            anchors.fill: parent
                        }
                    }
                }

                Tab {
                    id: featuresTab
                    objectName: "featuresTab"
                    title: "Features"
                    anchors.margins: 10
                    ColumnLayout {
                        RowLayout {
                            CheckBox {
                                id: ngramsFrom
                                text: "n-grams from"
                            }
                            SpinBox {
                                minimumValue: 1
                                maximumValue: 20
                                enabled: ngramsFrom.checked
                            }
                            Label {
                                text: "to"
                            }
                            SpinBox {
                                minimumValue: 1
                                maximumValue: 20
                                value: 3
                                enabled: ngramsFrom.checked
                            }
                        }
                        RowLayout {
                            anchors.left: parent.left
                            anchors.leftMargin: 10
                            Label {
                                text: "with document frecuency contraints:"
                            }
                        }
                        RowLayout {
                            anchors.left: parent.left
                            anchors.leftMargin: 20
                            CheckBox {
                                id: aMinimumDFOf
                                text: "a minimum of"
                                enabled: ngramsFrom.checked
                            }
                            SpinBox {
                                minimumValue: 1
                                maximumValue: 99999999
                                enabled: aMinimumDFOf.checked
                            }
                            ComboBox {
                                model: ["no. of documents", "% of documents"]
                            }
                        }
                        RowLayout {
                            anchors.left: parent.left
                            anchors.leftMargin: 20
                            CheckBox {
                                id: aMaximumDFOf
                                text: "a maximum of"
                                enabled: ngramsFrom.checked
                            }
                            SpinBox {
                                minimumValue: 1
                                maximumValue: 99999999
                                value: 100
                                enabled: aMaximumDFOf.checked
                            }
                            ComboBox {
                                currentIndex: 1
                                model: ["no. of documents", "% of documents"]
                            }
                        }
                        RowLayout {
                            anchors.left: parent.left
                            anchors.leftMargin: 10
                            CheckBox {
                                id: onlyMostSignificant
                                text: "only most significant"
                            }
                            SpinBox {
                                minimumValue: 1
                                maximumValue: 1000
                                value: 300
                                enabled: onlyMostSignificant.checked
                            }
                            Label {
                                text: "features"
                            }
                        }
                        RowLayout {
                            CheckBox {
                                id: removeFeaturesWithLessThan
                                text: "remove features with less than"
                            }
                            SpinBox {
                                decimals: 2
                                value: 0.10
                                minimumValue: 0
                                maximumValue: 99999999
                                enabled: removeFeaturesWithLessThan.checked
                            }
                            Label {
                                text: "variance"
                            }
                        }
                        RowLayout {
                            Button {
                                text: "RUN"
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
                    id: learnTab
                    objectName: "learnTab"
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
                    id: classifyTab
                    objectName: "classifyTab"
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
                    id: testTab
                    objectName: "testTab"
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
                    id: evaluateTab
                    objectName: "evaluateTab"
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

                model: current_model
                onCurrentRowChanged:  {
                }

                onModelChanged: {
                    console.log("numero es " + mainPfcsamrApp.rowCount)
                    console.log("numero es " + current_model.rowCount)
                    console.log("numero es " + model.rowCount)
                    console.log("KIYOOOOO")
                    console.log(model.data)
                    console.log(current_model)
                    console.log(model)
                    console.log("numero es " + current_model.rowCount())
                    console.log("numero es " + model.rowCount())
                    var table_headings = mainPfcsamrApp.get_table_headings()
                    var ii = 0
                    for (var p in model) {
                        console.log(p)
                    }
                    for (var pp in model.prototype) {
                        console.log(pp)
                    }
                    console.log(model.prototype)

                    console.log('model.count is ' + model.count)
                    for (ii = 0; ii < model.count; ii++) {
                        for (var i = 0; i < table_headings.length; i++) {
                            console.log("setting " + table_headings[i] + " of " + ii)
                            model.setProperty(ii, table_headings[i],
                                              "Something")
                        }
                    }
                    for (var j = 0; j < table_headings.length; j++) {
                        addColumn(Qt.createQmlObject(
                                      'import QtQuick 2.2; import QtQuick.Controls 1.3; import QtQuick.Layouts 1.1;'
                                      + 'TableViewColumn{' + 'role: "' + table_headings[j]
                                      + '";' + 'title: "' + table_headings[j]
                                      + '";' + ' width: 100;' + ' }',
                                      data_table_view))
                        console.log('import QtQuick 2.2; import QtQuick.Controls 1.3; import QtQuick.Layouts 1.1;' + 'TableViewColumn{'
                                    + 'role: "' + table_headings[j] + '";' + 'title: "'
                                    + table_headings[j] + '";' + ' width: 100;' + ' }')
                    }
                }
            }
        }
    }
}
