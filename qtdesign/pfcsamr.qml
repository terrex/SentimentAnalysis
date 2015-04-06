import QtQuick 2.0
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.3
import QtQuick.Window 2.2
import QtQuick.Dialogs 1.2
import pfcsamr 1.0

ApplicationWindow {
    id: rootWindow
    width: 640
    height: 480

    MainPfcsamrApp {
        id: mainPfcsamrApp

    }

    FileDialog {
        id: fileDialogChooseTSV
        nameFilters: ["Tab-separated files (*.tsv)"]
        onAccepted: mainPfcsamrApp.load_tsv(fileDialogChooseTSV.fileUrl)
    }

    menuBar: MenuBar {
        Menu {
            title: "File"
            MenuItem { text: "Open..." }
            MenuItem {
                text: "Load .tsv..."
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

    Button {
        id: button1
        y: 67
        text: qsTr("Botón")
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }
}
