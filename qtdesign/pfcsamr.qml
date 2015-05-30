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

    TabView {
        anchors.fill: parent

        Tab {
            id: designTab
            objectName: "designTab"
            title: "Design"

            TextArea {
                id: txtProgram
                objectName: "txtProgram"
                anchors.fill: parent
                textFormat: TextEdit.AutoText
            }
        }

        Tab {
            id: runTab
            objectName: "runTab"
            title: "Run"
        }

        onCurrentIndexChanged: {
            if (currentIndex == 0) {
                rootWindow.toolBar = designTabToolbar
                designTabToolbar.visible = true
                runTabToolbar.visible = false
                emptyToolbar.visible = false
            } else if (currentIndex == 1) {
                rootWindow.toolBar = runTabToolbar
                designTabToolbar.visible = false
                runTabToolbar.visible = true
                emptyToolbar.visible = false
            }
        }
    }

    ToolBar {
        id: emptyToolbar
        objectName: "emptyToolbar"
        visible: false

        RowLayout {
            Item {
                Layout.fillWidth: true
            }
        }
    }

    ToolBar {
        id: runTabToolbar
        objectName: "runTabToolbar"
        visible: false

        RowLayout {
            anchors.fill: parent
            ToolButton {
                id: btnRun
                objectName: "btnRun"
                text: qsTr("Run")
                onClicked: mainPfcsamrApp.run_script()
            }
        }
    }

    toolBar: ToolBar {
        id: designTabToolbar
        objectName: "designTabToolbar"

        RowLayout {
            anchors.fill: parent
            ToolButton {
                id: btnOpenTrain
                objectName: "btnOpenTrain"
                text: qsTr("Open train.tsv")
                onClicked: fileDialogChooseTSV.open()
            }
            ToolButton {
                text: qsTr("Remove contractions")
                onClicked: mainPfcsamrApp.remove_contractions()
            }
            ToolButton {
                text: qsTr("Tokenize")
                onClicked: mainPfcsamrApp.tokenize()
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
            ToolButton {
                text: qsTr("word2vec")
                onClicked: mainPfcsamrApp.word2vec()
            }
            ToolButton {
                text: qsTr("vectorize")
                onClicked: mainPfcsamrApp.vectorize()
            }
        }
    }
}
