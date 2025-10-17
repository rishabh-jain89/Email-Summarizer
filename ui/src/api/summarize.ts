export interface EmailSummaryResponse {
    summary: {
        main_points: string[];
        action_items: string[];
    };
}

export async function summarizeEmail(emailText: string): Promise<EmailSummaryResponse> {
    const response = await fetch("https://email-summarizer-backend.onrender.com/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email_text: emailText }),
    });

    if (!response.ok) {
        throw new Error(`Backend error: ${response.statusText}`);
    }

    return response.json();
}

