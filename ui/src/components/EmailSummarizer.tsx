"use client";
import { useState, useEffect } from "react";
import { summarizeEmail, EmailSummaryResponse } from "../api/summarize";
import { useCopilotContext } from "@copilotkit/react-core";


type SummaryData = EmailSummaryResponse['summary'];

export default function EmailSummarizer() {
    const [emailText, setEmailText] = useState("");
    const [summary, setSummary] = useState<SummaryData | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const copilot = useCopilotContext();
    useEffect(() => {
    }, [copilot]);

    const handleSummarize = async () => {
        if (!emailText.trim()) return;
        setLoading(true);
        setSummary(null);
        setError(null);

        try {
            const result = await summarizeEmail(emailText);
            setSummary(result.summary);

            copilot.addContext(`emailText: ${emailText}`);

            copilot.addContext(
                `summary: ${JSON.stringify({
                    main_points: result.summary.main_points || [],
                    action_items: result.summary.action_items || [],
                })}`
            );

            const internalContext = copilot.getAllContext?.() || [];


        } catch (err: any) {
            console.error(err);
            setError(err.message || "An unexpected error occurred.");
        } finally {
            setLoading(false);
        }
    };

    const SummarySkeleton = () => (
        <div className="space-y-4 animate-pulse w-full px-4">
            <div className="h-4 bg-gray-300 rounded w-1/3"></div>
            <div className="space-y-2">
                <div className="h-3 bg-gray-300 rounded w-full"></div>
                <div className="h-3 bg-gray-300 rounded w-5/6"></div>
            </div>
            <div className="h-4 bg-gray-300 rounded w-1/4 pt-4"></div>
            <div className="space-y-2">
                <div className="h-3 bg-gray-300 rounded w-full"></div>
                <div className="h-3 bg-gray-300 rounded w-4/6"></div>
            </div>
        </div>
    );

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8 w-full">
            <div className="flex flex-col space-y-4">
                <h2 className="text-xl font-bold text-gray-800">Your Email</h2>
                <textarea
                    className="w-full flex-grow h-96 p-4 border border-gray-300/50 bg-white/80 rounded-lg shadow-inner focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none resize-none text-gray-800 transition-shadow"
                    placeholder="Paste your email text here..."
                    value={emailText}
                    onChange={(e) => setEmailText(e.target.value)}
                />
                <button
                    onClick={handleSummarize}
                    disabled={loading || !emailText.trim()}
                    className="w-full py-3 px-4 font-semibold text-white rounded-lg shadow-md transition-all duration-300 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                    {loading ? "Summarizing..." : "Summarize Email"}
                </button>
            </div>

            <div className="flex flex-col space-y-4">
                <h2 className="text-xl font-bold text-gray-800">Summary</h2>
                <div className="w-full flex-grow h-96 p-4 border border-gray-300/50 rounded-lg bg-white/100 shadow-inner flex flex-col justify-center items-center transition-all duration-300">
                    {loading ? (
                        <SummarySkeleton />
                    ) : error ? (
                        <div className="text-center text-red-600 p-4">
                            <p className="font-bold text-lg">An Error Occurred</p>
                            <p className="text-sm text-red-500 mt-1">{error}</p>
                        </div>
                    ) : summary ? (
                        <div className="w-full h-full overflow-y-auto text-gray-800 p-2 prose prose-sm max-w-none">
                            <h3 className="font-semibold text-gray-900">Main Points:</h3>
                            <ul className="list-disc list-outside pl-5">
                                {summary.main_points?.map((point, i) => (
                                    <li key={`point-${i}`} className="mb-1">{point}</li>
                                ))}
                            </ul>

                            {summary.action_items?.length > 0 && (
                                <>
                                    <h3 className="font-semibold mt-4 text-gray-900">Action Items:</h3>
                                    <ul className="list-disc list-outside pl-5">
                                        {summary.action_items.map((item, i) => (
                                            <li key={`item-${i}`} className="mb-1">{item}</li>
                                        ))}
                                    </ul>
                                </>
                            )}
                        </div>
                    ) : (
                        <div className="text-center text-gray-500 p-4">
                            <p className="font-semibold text-lg">Your summary will appear here</p>
                            <p className="mt-1">Paste an email on the left and click the button to see the magic happen!</p>
                        </div>
                    )}
                </div>
            </div>
        </div>

    );
}

