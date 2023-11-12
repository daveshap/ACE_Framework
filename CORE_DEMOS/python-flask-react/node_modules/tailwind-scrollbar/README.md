# Scrollbar Plugin for Tailwind CSS
![Tests](https://github.com/adoxography/tailwind-scrollbar/workflows/Tests/badge.svg)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/af892fe4afc048c4860462c5fc736675)](https://www.codacy.com/gh/adoxography/tailwind-scrollbar/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=adoxography/tailwind-scrollbar&amp;utm_campaign=Badge_Grade)
![npm](https://img.shields.io/npm/dt/tailwind-scrollbar)

Adds styling utilities for scrollbars in Firefox and webkit-based browsers.

## Installation

```bash
yarn add -D tailwind-scrollbar
```
or
```bash
npm install --save-dev tailwind-scrollbar
```

Add it to the plugins array of your Tailwind config.

```js
plugins: [
    // ...
    require('tailwind-scrollbar'),
],
```

## Usage

**NB:** This plugin *styles* scrollbars; it does not force them to appear. Use typical CSS techniques to force content to overflow and trigger a scrollbar.

For every element that you want to style, add either the `scrollbar` or `scrollbar-thin` class. You may then add any `scrollbar-track-{color}`, `scrollbar-thumb-{color}` or `hover:scrollbar-thumb-{color}` classes you like. (Note that `hover:scrollbar-thumb-{color}` classes only have effects in webkit-based browsers.)

If you're using both vertical and horizontal scrollbars, you may notice a white square show up. You can change its colour with the `scrollbar-corner-{color}` utility.

Here's a minimal example (keeping in mind that the `h-32` and `h-64` classes are just there to force the scrollbar to appear):

```html
<div class="h-32 scrollbar scrollbar-thumb-gray-900 scrollbar-track-gray-100">
    <div class="h-64"></div>
</div>
```

A live version of this demo [can be found here](https://tailwind-scrollbar-example.adoxography.repl.co/).

## Configuration

This plugin is capable of adding utilties for creating rounded scrollbars by referencing your configured [border radius](https://tailwindcss.com/docs/border-radius#customizing) settings. However, as they are only supported in chromium-based browsers, their usage is inadvisable in cross-browser applications. To enable rounded scrollbar utilities, pass `nocompatible: true` to the plugin during its declaration; e.g.:

```js
plugins: [
    // ...
    require('tailwind-scrollbar')({ nocompatible: true }),
],
```

This will add utilities such as `scrollbar-thumb-rounded` or `scrollbar-thumb-rounded-md`.

## Complete list of utilities
All utilities are compatible with variants, unless otherwise specified.

### Width utilities
These utilities initialize scrollbar styling. You always need one of them, even if you're using custom widths. (See below.)

| Utility     | Effect | Notes |
|-------------|--------|-------|
| `scrollbar` | Enables custom scrollbar styling, using the default width | On Firefox, this is `scrollbar-width: auto`, which is `16px`. Chrome is hard coded to `16px` for consistency. |
| `scrollbar-thin` | Enables custom scrollbar styling, using the thin width | On Firefox, this is `scrollbar-width: thin`, which is `8px`. Chrome is hard coded to `8px` for consistency. |
| `scrollbar-none` | Hides the scrollbar completely | Because of browser quirks, this cannot be used to hide an existing styled scrollbar - i.e. `scrollbar hover:scrollbar-none` will not work. |

### Colour utilities
All of the asterisks can be replaced [with any tailwind colour](https://tailwindcss.com/docs/customizing-colors#using-custom-colors), including [arbitrary values](https://tailwindcss.com/docs/adding-custom-styles#using-arbitrary-values) and [opacity modifiers](https://tailwindcss.com/docs/background-color#changing-the-opacity). With the exception of the width utilities, all utilities are inherited by child elements.

| Utility     | Effect | Notes |
|-------------|--------|-------|
| `scrollbar-thumb-*` | Sets the colour of the scrollbar thumb | |
| `scrollbar-track-*` | Sets the colour of the scrollbar track | |
| `scrollbar-corner-*` | Sets the colour of the scrollbar corner | The corner will only appear if you have both vertical and horizontal scrollbars. |

### Nocompatible utilities
These styles are only available in `nocompatible` mode. They won't have any effect in Firefox.

| Utility     | Effect | Notes |
|-------------|--------|-------|
| `scrollbar-w-*` | Sets the width of vertical scrollbars | The asterisk can be replaced with any Tailwind [width setting](https://tailwindcss.com/docs/width), including arbitrary values. Only applies to scrollbars styled with `scrollbar` (not `scrollbar-thin`). |
| `scrollbar-h-*` | Sets the height of horizontal scrollbars | The asterisk can be replaced with any Tailwind [height setting](https://tailwindcss.com/docs/height), including arbitrary values. Only applies to scrollbars styled with `scrollbar` (not `scrollbar-thin`). |
| `scrollbar-rounded-*` | Rounds a scrollbar thumb's corners | The asterisk can be replaced with any Tailwind [rounded setting](https://tailwindcss.com/docs/border-radius#using-custom-values), including arbitrary values. |

## License

This project is licensed under the [MIT License](/LICENSE).
