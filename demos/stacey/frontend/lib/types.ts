// Make sure this stays in sync with the server-side version (types.py)

import {format, utcToZonedTime} from "date-fns-tz";

export interface ChatMessage {
    sender: string;
    content: string;
    time_utc: string; // formatted like 2023-01-30T13:45:00Z
}

export function createChatMessage(sender: string, content: string): ChatMessage {
    const utcDate = utcToZonedTime(new Date(), 'Etc/UTC');
    const formattedDate = format(utcDate, "yyyy-MM-dd'T'HH:mm:ss'Z'", { timeZone: 'Etc/UTC' });
    return {
        sender: sender,
        content: content,
        time_utc: formattedDate
    };
}