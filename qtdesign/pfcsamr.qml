import QtQuick 2.0
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.3
import QtQuick.Window 2.2
import QtQuick.Dialogs 1.2

ApplicationWindow {
    id: rootWindow
    width: 640
    height: 480

    FileDialog {
        id: fileDialogChooseTSV
        nameFilters: ["Tab-separated files (*.tsv)"]
        onAccepted: mainPfcsamrApp.load_tsv(fileDialogChooseTSV.fileUrl.toString())
    }

    TextEdit {
        id: textEdit1
        x: 13
        y: 39
        width: 518
        height: 199
        text: qsTr("Text Edit")
        font.pixelSize: 12
    }

    menuBar: MenuBar {
        Menu {
            title: "File"
            MenuItem { text: "Open..." }
            MenuItem {
                text: "Load train.tsv..."
                onTriggered: fileDialogChooseTSV.open()
            }
            MenuItem { text: "Close" }
        }

        Menu {
            title: "Edit"
            MenuItem { text: "Cut" }
            MenuItem { text: "Copy" }
            MenuItem { text: "Paste" }
        }
    }
}
