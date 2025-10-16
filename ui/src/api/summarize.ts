export interface EmailSummaryResponse {
    summary: {
        main_points: string[];
        action_items: string[];
    };
}

export async function summarizeEmail(emailText: string): Promise<EmailSummaryResponse> {
    const response = await fetch("http://127.0.0.1:8000/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email_text: emailText }),
    });

    if (!response.ok) {
        throw new Error(`Backend error: ${response.statusText}`);
    }

    return response.json();
}

