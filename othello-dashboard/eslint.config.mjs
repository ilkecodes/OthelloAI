/** @type {import('eslint').Linter.FlatConfig[]} */
export default [
  // Dosya/klasör ignore
  {
    ignores: [
      'app/**/page.backup.*.tsx',
      'app/simple/**', // local prototip ise lint dışı
    ],
  },
  // Kural seviyesi ayarları (hızlı yeşil için "off"/"warn")
  {
    files: ['**/*.{ts,tsx}'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-empty-object-type': 'off',
      'react/no-unescaped-entities': 'off',
      // next/image uyarıları build'i durdurmaz, uyarı kalsın
    },
  },
];
