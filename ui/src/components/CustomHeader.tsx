"use client";
import { X } from "lucide-react";

const CustomHeader = ({
                          labels,
                          onClose,
                      }: {
    labels?: { title?: string };
    onClose?: () => void;
}) => {
    return (
        <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-white">
            <h2 className="text-lg font-bold text-gray-800 font-sans tracking-wide">
                {labels?.title || "Assistant"}
            </h2>
            {onClose && (
                <button
                    onClick={onClose}
                    className="text-gray-500 hover:text-gray-800 focus:outline-none"
                    aria-label="Close chat"
                >
                    <X size={22} />
                </button>
            )}
        </div>
    );
};

export default CustomHeader;
