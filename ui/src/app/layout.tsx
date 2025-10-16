"use client";
import "./globals.css";
import CopilotProvider from "../components/CopilotProvider";
import "@copilotkit/react-ui/styles.css";

export default function RootLayout({children,}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
        <body>
        <CopilotProvider>{children}</CopilotProvider>
        </body>
        </html>
    );
}
