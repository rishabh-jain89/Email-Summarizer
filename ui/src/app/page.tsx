"use client";

import EmailSummarizer from "../components/EmailSummarizer";

export default function Page() {
    return (
        <main className="min-h-screen flex items-center justify-center  p-4 md:p-8">
            <div className="max-w-6xl w-full  rounded-xl shadow-[0_0_10px_rgba(0,0,0,0.25)] p-6 md:p-10">
                <header className="text-center mb-8">
                    <h1 className="text-3xl md:text-5xl font-serif text-gray-800">
                        Email Summarizer
                    </h1>
                </header>
                <EmailSummarizer />
            </div>
        </main>
    );
}
