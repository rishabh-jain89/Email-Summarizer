"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui";
import CustomHeader from "./CustomHeader";
import "@copilotkit/react-ui/styles.css";

export default function CopilotProvider({
                                            children,
                                        }: {
    children: React.ReactNode;
}) {
    return (
        <CopilotKit runtimeUrl="http://127.0.0.1:8000/chat">
            {children}

            <CopilotPopup
                labels={{
                    title: "Email Agent",
                    initial: "Hello! How are you?",
                }}
                hitEscapeToClose={true}
                Header={CustomHeader}

            />
        </CopilotKit>
    );
}
