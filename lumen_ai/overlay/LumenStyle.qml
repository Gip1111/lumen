import QtQuick 2.15

pragma Singleton

QtObject {
    // Colors
    readonly property color accent: "#3498db"
    readonly property color bgPrimary: "#cc1a1a1a" // Glassmorphism dark
    readonly property color bgSecondary: "#33ffffff"
    readonly property color textPrimary: "#ffffff"
    readonly property color textSecondary: "#b3ffffff"
    readonly property color border: "#40ffffff"
    
    // Gradients
    readonly property var mainGradient: [
        { position: 0.0, color: "#2980b9" },
        { position: 1.0, color: "#6dd5fa" }
    ]
    
    // Spacing
    readonly property int padding: 16
    readonly property int radius: 12
    
    // Typography
    readonly property string fontFamily: "Inter"
    readonly property int fontSizeHeader: 18
    readonly property int fontSizeBody: 14
}
