export function parseHexColors(text: string): string[] {
    const hexColorRegex = /#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})/g;
    const matches = text.match(hexColorRegex);
    return matches ? matches : [];
}