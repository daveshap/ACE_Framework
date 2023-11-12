/**
 * Base resets to make the plugin's utilities work
 */
export const BASE_STYLES: {
    '*': {
        'scrollbar-color': string;
        'scrollbar-width': string;
    };
};
/**
 * Utilities for initializing a custom styled scrollbar, which implicitly set
 * the scrollbar's size
 */
export const SCROLLBAR_SIZE_UTILITIES: {
    '.scrollbar': any;
    '.scrollbar-thin': any;
    '.scrollbar-none': {
        'scrollbar-width': string;
        '&::-webkit-scrollbar': {
            display: string;
        };
    };
};
/**
 * Adds scrollbar-COMPONENT-COLOR utilities for every scrollbar component.
 *
 * @param {typedefs.TailwindPlugin} tailwind - Tailwind's plugin object
 */
export function addColorUtilities({ matchUtilities, theme }: typedefs.TailwindPlugin): void;
/**
 * Adds scrollbar-COMPONENT-rounded-VALUE utilities for every scrollbar
 * component.
 *
 * @param {typedefs.TailwindPlugin} tailwind - Tailwind's plugin object
 */
export function addRoundedUtilities({ theme, matchUtilities }: typedefs.TailwindPlugin): void;
/**
 * Adds scrollbar-w-* and scrollbar-h-* utilities
 *
 * @param {typedefs.TailwindPlugin} tailwind - Tailwind's plugin object
 */
export function addSizeUtilities({ matchUtilities, theme }: typedefs.TailwindPlugin): void;
import typedefs = require("./typedefs");
