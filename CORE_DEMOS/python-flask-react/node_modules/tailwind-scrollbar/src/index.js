const plugin = require('tailwindcss/plugin');
const {
  BASE_STYLES,
  SCROLLBAR_SIZE_UTILITIES,
  addColorUtilities,
  addRoundedUtilities,
  addSizeUtilities
} = require('./utilities');
const { addVariantOverrides } = require('./variants');

module.exports = plugin.withOptions((options = {}) => tailwind => {
  tailwind.addBase(BASE_STYLES);
  tailwind.addUtilities(SCROLLBAR_SIZE_UTILITIES);
  addColorUtilities(tailwind);
  addVariantOverrides(tailwind);

  if (options.nocompatible) {
    addRoundedUtilities(tailwind);
    addSizeUtilities(tailwind);
  }
});
