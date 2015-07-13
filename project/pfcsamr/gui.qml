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
            ProgressBar {
                anchors.right: status_bar_count.left
                id: status_bar_progress
                objectName: 'status_bar_progress'
                width: 100
                minimumValue: 0
                maximumValue: 100
                value: 0
            }
            Label {
                anchors.right: parent.right
                id: status_bar_count
                objectName: "status_bar_count"
                text: mainPfcsamrApp.status_count
                width: 150
                horizontalAlignment: Label.AlignRight
                onTextChanged: {
                    status_bar_progress.maximumValue = Math.max(
                                status_bar_progress.maximumValue, text)
                    status_bar_progress.value = text
                }
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
                    enabled: mainPfcsamrApp.load_tab_enabled
                    ColumnLayout {
                        RowLayout {
                            Button {
                                text: "Select file"
                                onClicked: fileDialogChooseTSV.open()
                            }
                            TextEdit {
                                id: load_train_file
                                objectName: "load_train_file"
                                text: get_prop(objectName)
                                Layout.fillWidth: true
                                readOnly: true
                                onTextChanged: set_prop(objectName, text)
                            }
                        }
                        RowLayout {
                            CheckBox {
                                id: load_only_first
                                objectName: 'load_only_first'
                                text: "Load only first"
                                checked: get_prop(objectName)
                                onCheckedChanged: set_prop(objectName, checked)
                            }
                            SpinBox {
                                id: load_only_first_rows
                                objectName: 'load_only_first_rows'
                                enabled: load_only_first.checked
                                minimumValue: 0
                                maximumValue: 99999999 //Actualizar por código
                                value: get_prop(objectName)
                                onValueChanged: set_prop(objectName, value)
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
                                onClicked: {
                                    status_bar_progress.maximumValue = 100
                                    mainPfcsamrApp.load_button_load_on_clicked()
                                }
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
                    enabled: mainPfcsamrApp.preproc_tab_enabled
                    ColumnLayout {
                        CheckBox {
                            id: preproc_unsplit_contractions
                            objectName: 'preproc_unsplit_contractions'
                            text: "unsplit contractions"
                            checked: get_prop(objectName)
                            onCheckedChanged: set_prop(objectName, checked)
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
                            checked: get_prop(objectName)
                            onCheckedChanged: set_prop(objectName, checked)
                        }
                        CheckBox {
                            id: preproc_remove_stopwords
                            objectName: 'preproc_remove_stopwords'
                            text: "remove stopwords"
                            checked: get_prop(objectName)
                            onCheckedChanged: set_prop(objectName, checked)
                        }
                        GroupBox {
                            id: preproc_word_replacement
                            objectName: 'preproc_word_replacement'
                            checkable: true
                            title: "word replacement"
                            checked: get_prop(objectName)
                            onCheckedChanged: set_prop(objectName, checked)
                            ExclusiveGroup {
                                id: stemmizeLemmatizeExclusiveGroup
                            }
                            ColumnLayout {
                                RadioButton {
                                    id: preproc_stemmize
                                    objectName: 'preproc_stemmize'
                                    text: "stemmize"
                                    exclusiveGroup: stemmizeLemmatizeExclusiveGroup
                                    checked: get_prop(objectName)
                                    onCheckedChanged: set_prop(objectName,
                                                               checked)
                                }
                                RadioButton {
                                    id: preproc_lemmatize
                                    objectName: 'preproc_lemmatize'
                                    text: "lemmatize"
                                    exclusiveGroup: stemmizeLemmatizeExclusiveGroup
                                    checked: get_prop(objectName)
                                    onCheckedChanged: set_prop(objectName,
                                                               checked)
                                }
                            }
                        }
                        CheckBox {
                            id: preproc_pos_tag_words
                            objectName: 'preproc_pos_tag_words'
                            text: "POS tag words"
                            checked: get_prop(objectName)
                            onCheckedChanged: set_prop(objectName, checked)
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
                    enabled: mainPfcsamrApp.features_tab_enabled
                    ColumnLayout {
                        RowLayout {
                            CheckBox {
                                id: features_ngrams
                                objectName: 'features_ngrams'
                                text: "n-grams from"
                                checked: get_prop(objectName)
                                onCheckedChanged: set_prop(objectName, checked)
                            }
                            SpinBox {
                                id: features_ngrams_from
                                objectName: 'features_ngrams_from'
                                minimumValue: 1
                                maximumValue: Math.min(20,
                                                       features_ngrams_to.value)
                                enabled: features_ngrams.checked
                                value: get_prop(objectName)
                                onValueChanged: set_prop(objectName, value)
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
                                value: get_prop(objectName)
                                onValueChanged: set_prop(objectName, value)
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
                                checked: get_prop(objectName)
                                onCheckedChanged: set_prop(objectName, checked)
                                onEnabledChanged: if (!enabled)
                                                      checked = false
                            }
                            SpinBox {
                                id: features_minimum_df_value
                                objectName: 'features_minimum_df_value'
                                minimumValue: 1
                                maximumValue: 99999999
                                enabled: features_minimum_df.checked
                                value: get_prop(objectName)
                                onValueChanged: set_prop(objectName, value)
                            }
                            ComboBox {
                                id: features_minimum_df_unit
                                objectName: 'features_minimum_df_unit'
                                model: ["no. of documents", "% of documents"]
                                enabled: features_minimum_df.checked
                                currentIndex: get_prop(objectName)
                                onCurrentIndexChanged: set_prop(objectName,
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
                                checked: get_prop(objectName)
                                onCheckedChanged: set_prop(objectName, checked)
                            }
                            SpinBox {
                                id: features_maximum_df_value
                                objectName: 'features_maximum_df_value'
                                minimumValue: 1
                                maximumValue: 99999999
                                enabled: features_maximum_df.checked
                                value: get_prop(objectName)
                                onValueChanged: set_prop(objectName, value)
                            }
                            ComboBox {
                                id: features_maximum_df_unit
                                objectName: 'features_maximum_df_unit'
                                model: ["no. of documents", "% of documents"]
                                enabled: features_maximum_df.checked
                                currentIndex: get_prop(objectName)
                                onCurrentIndexChanged: set_prop(objectName,
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
                                checked: get_prop(objectName)
                                onCheckedChanged: set_prop(objectName, checked)
                            }
                            SpinBox {
                                id: features_only_most_significant_feats
                                objectName: 'features_only_most_significant_feats'
                                minimumValue: 1
                                maximumValue: 1000
                                enabled: features_only_most_significant.checked
                                value: get_prop(objectName)
                                onValueChanged: set_prop(objectName, value)
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
                                checked: get_prop(objectName)
                                onCheckedChanged: set_prop(objectName, checked)
                            }
                            SpinBox {
                                id: features_remove_less_than_variance
                                objectName: 'features_remove_less_than_variance'
                                decimals: 2
                                stepSize: 0.01
                                minimumValue: 0
                                maximumValue: 99999999
                                enabled: features_remove_less_than.checked
                                value: get_prop(objectName)
                                onValueChanged: set_prop(objectName, value)
                            }
                            Label {
                                text: "variance"
                                enabled: features_remove_less_than.checked
                            }
                            Label {
                                id: variance_warn_message_id
                                text: mainPfcsamrApp.variance_warn_message
                                color: "red"
                                font.capitalization: Font.AllUppercase
                                Behavior on text {
                                    SequentialAnimation {
                                        running: false
                                        loops: 5
                                        ColorAnimation {
                                            target: variance_warn_message_id
                                            property: "color"
                                            from: "red"
                                            to: "white"
                                            duration: 500
                                        }
                                        ColorAnimation {
                                            target: variance_warn_message_id
                                            property: "color"
                                            from: "white"
                                            to: "red"
                                            duration: 500
                                        }
                                    }
                                }
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
                    enabled: mainPfcsamrApp.learn_tab_enabled
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
                                                id: learn_multinomialnb_alpha
                                                objectName: 'learn_multinomialnb_alpha'
                                                minimumValue: 0.00
                                                maximumValue: 1.00
                                                decimals: 2
                                                stepSize: 0.1
                                                value: get_prop(objectName)
                                                onValueChanged: set_prop(
                                                                    objectName,
                                                                    value)
                                            }
                                        }
                                        CheckBox {
                                            id: learn_multinomialnb_fit_prior
                                            objectName: 'learn_multinomialnb_fit_prior'
                                            text: "learn class priors"
                                            checked: get_prop(objectName)
                                            onCheckedChanged: set_prop(
                                                                  objectName,
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
                                                                  bjectName + '_idx')
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
                    enabled: mainPfcsamrApp.classify_tab_enabled
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
                    enabled: mainPfcsamrApp.test_tab_enabled
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
                    enabled: mainPfcsamrApp.evaluate_tab_enabled
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

                    if (model !== undefined) {
                        for (var j = 0; j < model.columnCount(); j++) {
                            var roleName = model.headerData(j, Qt.Horizontal)
                            addColumn(Qt.createQmlObject(
                                          'import QtQuick 2.2; import QtQuick.Controls 1.3; import QtQuick.Layouts 1.1;'
                                          + 'TableViewColumn{role:"' + roleName
                                          + '";title:"' + roleName + '";width:100;}',
                                          data_table_view))
                        }
                        resizeColumnsToContents()
                    } else {
                        console.log("model is undefined")
                    }
                }
            }
        }
    }
}
