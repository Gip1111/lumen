import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtGraphicalEffects 1.15

ApplicationWindow {
    id: window
    visible: true
    width: 800
    height: 600
    color: "transparent"
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint

    // Background Dimming
    Rectangle {
        anchors.fill: parent
        color: "#40000000"
        opacity: 0
        Behavior on opacity { NumberAnimation { duration: 200 } }
        Component.onCompleted: opacity = 1
    }

    // Main Container
    Rectangle {
        id: container
        width: 700
        height: inputArea.height + (chatList.count > 0 ? 400 : 0)
        anchors.centerIn: parent
        radius: 16
        color: "#cc1a1a1a" // Glass dark
        border.color: "#33ffffff"
        border.width: 1
        clip: true

        Behavior on height { NumberAnimation { duration: 300; easing.type: Easing.OutCubic } }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20
            spacing: 15

            // Input Area
            RowLayout {
                id: inputArea
                Layout.fillWidth: true
                Layout.preferredHeight: 60
                spacing: 15

                Rectangle {
                    Layout.preferredWidth: 40
                    Layout.preferredHeight: 40
                    radius: 20
                    color: "#3498db"
                    
                    Text {
                        anchors.centerIn: parent
                        text: "L"
                        color: "white"
                        font.pixelSize: 20
                        font.bold: true
                    }
                }

                TextField {
                    id: queryInput
                    Layout.fillWidth: true
                    placeholderText: "How can I help you today?"
                    font.pixelSize: 18
                    color: "white"
                    background: null
                    onAccepted: {
                        if (text.length > 0) {
                            bridge.sendQuery(text)
                            text = ""
                        }
                    }
                }
            }

            // Chat/Result Area
            ListView {
                id: chatList
                Layout.fillWidth: true
                Layout.fillHeight: true
                visible: count > 0
                spacing: 10
                model: chatModel
                delegate: Column {
                    width: chatList.width
                    spacing: 5
                    
                    Text {
                        text: role === "user" ? "You" : "Lumen"
                        font.bold: true
                        font.pixelSize: 12
                        color: role === "user" ? "#3498db" : "#2ecc71"
                    }
                    
                    Text {
                        width: parent.width
                        text: content
                        color: "white"
                        font.pixelSize: 16
                        wrapMode: Text.WordWrap
                    }
                }
            }
        }
    }

    // Initial animation
    Component.onCompleted: {
        container.scale = 0.95
        container.opacity = 0
        var anim = SequentialAnimation {
            ParallelAnimation {
                NumberAnimation { target: container; property: "scale"; to: 1.0; duration: 250; easing.type: Easing.OutBack }
                NumberAnimation { target: container; property: "opacity"; to: 1.0; duration: 200 }
            }
        }
        anim.start()
    }
}
