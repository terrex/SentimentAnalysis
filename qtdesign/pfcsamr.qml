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
        onAccepted: mainPfcsamrApp.load_tsv(fileUrl)
    }

    ListModel {
        id: libraryModel
        ListElement {
            title: "A Masterpiece"
            author: "Gabriel"
        }
        ListElement {
            title: "Brilliance"
            author: "Jens"
        }
        ListElement {
            title: "Outstanding"
            author: "Frederik"
        }
    }

    SplitView {
        anchors.fill: parent
        orientation: Qt.Vertical

        Rectangle {
            Layout.minimumHeight: 300

            TabView {
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
                            }
                            TextEdit {
                                text: "No file selected"
                                Layout.fillWidth: true
                                readOnly: true
                            }
                        }
                        RowLayout {
                            CheckBox {
                                id: loadOnlyFirst
                                text: "Load only first"
                                checked: false
                            }
                            SpinBox {
                                enabled: loadOnlyFirst.checked
                                minimumValue: 0
                                maximumValue: 99999999 //Actualizar por código
                                value: 1000 //Actualizar por código
                            }
                            Label {
                                text: "samples"
                            }
                        }
                        RowLayout {
                            Button {
                                text: "LOAD"
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
                            id: unsplitContractions
                            text: "unsplit contractions"
                        }
                        CheckBox {
                            anchors.left: parent.left
                            anchors.leftMargin: 10
                            text: "expand contractions"
                            enabled: unsplitContractions.checked
                            onEnabledChanged: {
                                if (!enabled) {
                                    checked = false
                                }
                            }
                        }
                        CheckBox {
                            text: "remove stopwords"
                        }
                        GroupBox {
                            checkable: true
                            title: "word replacement"
                            checked: false
                            ExclusiveGroup {
                                id: stemmizeLemmatizeExclusiveGroup
                            }
                            ColumnLayout {
                                RadioButton {
                                    text: "stemmize"
                                    exclusiveGroup: stemmizeLemmatizeExclusiveGroup
                                }
                                RadioButton {
                                    text: "lemmatize"
                                    exclusiveGroup: stemmizeLemmatizeExclusiveGroup
                                    checked: true
                                }
                            }
                        }
                        CheckBox {
                            text: "POS tag words"
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
                anchors.fill: parent

                TableViewColumn {
                    role: "title"
                    title: "Title"
                }
                TableViewColumn {
                    role: "author"
                    title: "Author"
                }
                model: libraryModel
            }
        }
    }
}
