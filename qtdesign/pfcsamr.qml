import QtQuick 2.2
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.3
import QtQuick.Window 2.2
import QtQuick.Dialogs 1.2

ApplicationWindow {
    id: rootWindow
    objectName: "rootWindow"
    width: 640
    height: 480

    FileDialog {
        id: fileDialogChooseTSV
        objectName: "fileDialogChooseTSV"
        nameFilters: ["Tab-separated files (*.tsv)"]
        onAccepted: mainPfcsamrApp.load_tsv(fileUrl)
    }

    TextArea {
        id: txtProgram
        objectName: "txtProgram"
        anchors.fill: parent
        textFormat: TextEdit.AutoText
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

    toolBar: ToolBar {
        RowLayout {
            anchors.fill: parent
            ToolButton {
                id: btnOpenTrain
                objectName: "btnOpenTrain"
                text: qsTr("Open train.tsv")
                onClicked: fileDialogChooseTSV.open()
            }
            ToolButton {
                text: qsTr("Vectorize")
                onClicked: mainPfcsamrApp.vectorize()
            }
            ToolButton {
                text: qsTr("Remove stopwords")
                onClicked: mainPfcsamrApp.remove_stopwords()
            }
            ToolButton {
                text: qsTr("Stemmize")
                onClicked: mainPfcsamrApp.stemmize()
            }
            ToolButton {
                text: qsTr("Lemmatize")
                onClicked: mainPfcsamrApp.lemmatize()
            }
            ToolButton {
                text: qsTr("BOW")
                onClicked: mainPfcsamrApp.bow()
            }
            ToolButton {
                text: qsTr("2-BOW")
                onClicked: mainPfcsamrApp.bow_bigrams()
            }
        }
    }
}
