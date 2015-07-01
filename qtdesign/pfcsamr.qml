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

                    GridLayout {
                        columns: 1

                        RowLayout {
                            Button {
                                text: "Select file"
                            }
                            TextField {
                                width: 100
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
                                maximumValue: 1000 //Actualizar por código
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
                }

                Tab {
                    id: featuresTab
                    objectName: "featuresTab"
                    title: "Features"
                }

                Tab {
                    id: learnTab
                    objectName: "learnTab"
                    title: "Learn"
                }

                Tab {
                    id: classifyTab
                    objectName: "classifyTab"
                    title: "Classify"
                }

                Tab {
                    id: testTab
                    objectName: "testTab"
                    title: "Test"
                }

                Tab {
                    id: evaluateTab
                    objectName: "evaluateTab"
                    title: "Evaluate"
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

    statusBar: StatusBar {
    }
}
