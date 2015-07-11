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
    title: "Sentiment Analysis"

    function set_prop(name, value) {
        mainPfcsamrApp.set_config_prop_value(name, value)
    }

    function get_prop(name, value) {
        return mainPfcsamrApp.get_config_prop(name)
    }

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
            mainPfcsamrApp.findChild('load_train_file').text = fileUrl.toString(
                        ).replace("file://", "")
            mainPfcsamrApp.findChild('load_button_load').enabled = true
        }
    }

    statusBar: StatusBar {
        RowLayout {
            anchors.fill: parent
            Label {
                id: status_bar_label
                objectName: "status_bar_label"
                text: mainPfcsamrApp.status_text
            }
            Label {
                anchors.right: parent.right
                id: status_bar_count
                objectName: "status_bar_count"
                text: mainPfcsamrApp.status_count_text
                width: 150
                horizontalAlignment: Label.AlignRight
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
                    enabled: false
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
                    enabled: false
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
                    enabled: false
                    ColumnLayout {
                        RowLayout {
                            id: splitRandomlyRowLayout
                            CheckBox {
                                id: learn_train_split
                                objectName: 'learn_train_split'
                                text: "split randomly"
                                checked: get_prop(objectName)
                                onCheckedChanged: set_prop(objectName, checked)
                            }
                            SpinBox {
                                id: learn_train_split_value
                                objectName: 'learn_train_split_value'
                                minimumValue: 1
                                maximumValue: 99
                                suffix: " %"
                                enabled: learn_train_split.checked
                                value: get_prop(objectName) * 100
                                onValueChanged: set_prop(objectName) / 100
                            }
                            Label {
                                text: "dataset for train and remaining for self-test"
                            }
                        }

                        RowLayout {
                            height: parent.height - splitRandomlyRowLayout.height
                                    - learn_button_run.height
                            TabView {
                                id: learn_tabs
                                objectName: 'learn_tabs'
                                anchors.fill: parent
                                Layout.fillWidth: true
                                Layout.fillHeight: true

                                Tab {
                                    id: learn_multinomialnb
                                    objectName: 'learn_multinomialnb'
                                    title: "MultinomialNB"
                                    anchors.margins: 10
                                    ColumnLayout {
                                        RowLayout {
                                            Label {
                                                text: "alpha smoothing (LaPlace/Lidstone)"
                                            }
                                            SpinBox {
                                                minimumValue: 0.00
                                                maximumValue: 1.00
                                                decimals: 2
                                                stepSize: 0.01
                                                value: get_prop(
                                                           'learn_multinomialnb_alpha')
                                                onValueChanged: set_prop(
                                                                    'learn_multinomialnb_alpha',
                                                                    value)
                                            }
                                        }
                                        CheckBox {
                                            text: "learn class priors"
                                            checked: get_prop(
                                                         'learn_multinomialnb_fit_prior')
                                            onCheckedChanged: set_prop(
                                                                  'learn_multinomialnb_fit_prior',
                                                                  checked)
                                        }

                                        RowLayout {
                                            anchors.fill: parent
                                        }
                                        RowLayout {
                                            anchors.verticalCenter: parent.verticalCenter
                                            width: parent.width
                                            anchors.bottomMargin: 0
                                            Label {
                                                text: "SCORE: "
                                            }
                                            Label {
                                                id: selftest_score_multinomialnb
                                                objectName: 'selftest_score_multinomialnb'
                                                text: get_prop(objectName)
                                            }
                                        }
                                    }
                                }
                                Tab {
                                    id: learn_gaussiannb
                                    objectName: 'learn_gaussiannb'
                                    title: "GaussianNB"
                                    anchors.margins: 10
                                    ColumnLayout {
                                        Label {
                                            text: "No configurable parameters"
                                        }

                                        RowLayout {
                                            anchors.fill: parent
                                        }
                                    }
                                }
                                Tab {
                                    id: learn_lda
                                    objectName: 'learn_lda'
                                    title: "LDA"
                                    anchors.margins: 10
                                    ColumnLayout {
                                        RowLayout {
                                            Label {
                                                text: 'Solver'
                                            }
                                            ComboBox {
                                                width: 100
                                                id: learn_lda_solver
                                                objectName: 'learn_lda_solver'
                                                model: ListModel {
                                                    ListElement {
                                                        text: 'Singular value decomposition'
                                                        value: 'svd'
                                                    }

                                                    ListElement {
                                                        text: 'Least squares solution'
                                                        value: 'lsqr'
                                                    }
                                                    ListElement {
                                                        text: 'Eigenvalue decomposition'
                                                        value: 'eigen'
                                                    }
                                                }
                                                currentIndex: get_prop(
                                                                  objectName + '_idx')
                                                onCurrentIndexChanged: {
                                                    set_prop(objectName + '_idx',
                                                             currentIndex)
                                                    set_prop(objectName,
                                                             learn_lda_solver.model.get(
                                                                 currentIndex).value)
                                                }
                                            }
                                        }
                                        RowLayout {
                                            CheckBox {
                                                id: learn_lda_n_components
                                                objectName: 'learn_lda_n_components'
                                                text: "Number of components"
                                                checked: get_prop(objectName)
                                                onCheckedChanged: set_prop(
                                                                      objectName,
                                                                      checked)
                                            }
                                            SpinBox {
                                                id: learn_lda_n_components_value
                                                objectName: 'learn_lda_n_components_value'
                                                minimumValue: 1
                                                maximumValue: 3
                                                enabled: learn_lda_n_components.checked
                                                value: get_prop(objectName)
                                                onValueChanged: set_prop(
                                                                    objectName,
                                                                    value)
                                            }
                                        }
                                        CheckBox {
                                            id: learn_lda_store_covariance
                                            objectName: 'learn_lda_store_covariance'
                                            text: "Additionally compute class covariance matrix"
                                            checked: get_prop(objectName)
                                            onCheckedChanged: set_prop(
                                                                  objectName,
                                                                  checked)
                                        }

                                        RowLayout {
                                            anchors.fill: parent
                                        }
                                    }
                                }
                                Tab {
                                    id: learn_qda
                                    objectName: 'learn_qda'
                                    title: "QDA"
                                    anchors.margins: 10
                                    ColumnLayout {
                                        RowLayout {
                                            Text {
                                                text: "Regularize covariance estimate"
                                            }
                                            SpinBox {
                                                id: learn_qda_reg_param
                                                objectName: 'learn_qda_reg_param'
                                                minimumValue: 0.00
                                                maximumValue: 1.00
                                                stepSize: 0.01
                                                decimals: 2
                                                value: get_prop(objectName)
                                                onValueChanged: set_prop(
                                                                    objectName,
                                                                    value)
                                            }
                                        }

                                        RowLayout {
                                            anchors.fill: parent
                                        }
                                    }
                                }
                                Tab {
                                    id: learn_linearsvc
                                    objectName: 'learn_linearsvc'
                                    title: "LinearSVC"
                                    anchors.margins: 10
                                    ColumnLayout {
                                        CheckBox {
                                            id: learn_linearsvc_dual
                                            objectName: 'learn_linearsvc_dual'
                                            text: "Solve dual instead of the primal problem"
                                            checked: get_prop(objectName)
                                            onCheckedChanged: set_prop(
                                                                  objectName,
                                                                  checked)
                                        }
                                        RowLayout {
                                            Label {
                                                text: "Max iterations"
                                            }
                                            SpinBox {
                                                id: learn_linearsvc_max_iter
                                                objectName: 'learn_linearsvc_max_iter'
                                                minimumValue: 0
                                                maximumValue: 1000
                                                value: get_prop(objectName)
                                                onValueChanged: set_prop(
                                                                    objectName,
                                                                    value)
                                            }
                                        }

                                        RowLayout {
                                            anchors.fill: parent
                                        }
                                    }
                                }
                            }
                        }

                        Button {
                            id: learn_button_run
                            objectName: 'learn_button_run'
                            text: "RUN"
                            onClicked: mainPfcsamrApp.learn_button_run_on_clicked(
                                           learn_tabs.currentIndex)
                        }
                    }
                }

                Tab {
                    id: classify_tab
                    objectName: "classify_tab"
                    title: "Classify"
                    anchors.margins: 10
                    enabled: false
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
                    enabled: false
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
                    enabled: false
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
                model: mainPfcsamrApp.current_model

                onModelChanged: {
                    console.log("onModelChanged")
                    while (columnCount > 0) {
                        removeColumn(0)
                    }
                    var table_headings = mainPfcsamrApp.table_headings
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
