import { FlatCompat } from "@eslint/eslintrc";
import eslint from "@eslint/js";
import globals from "globals";
import pluginVue from "eslint-plugin-vue";
import tseslint from "typescript-eslint";


const compat = new FlatCompat({
    baseDirectory: import.meta.dirname,
    recommendedConfig: eslint.configs.recommended
});

export default [
    eslint.configs.recommended,
    ...tseslint.configs.recommendedTypeChecked,
    ...pluginVue.configs["flat/strongly-recommended"],

    ...compat.extends("@vue/eslint-config-typescript/recommended"),
    {
        plugins: {
            "@typescript-eslint": tseslint.plugin
        },
        languageOptions: {
            globals: globals.browser,
            parserOptions: {
                parser: tseslint.parser,
                project: "tsconfig.json",
                tsconfigRootDir: import.meta.dirname,
                extraFileExtensions: [".vue"]
            }
        }
    },
    {
        rules: {
            "@typescript-eslint/no-explicit-any": 0,
            "@typescript-eslint/no-empty-function": 0,
            "@typescript-eslint/ban-types": 0,
            "@typescript-eslint/no-unsafe-assignment": 0,
            "@typescript-eslint/no-unsafe-member-access": 0,
            "@typescript-eslint/no-unsafe-return": 0,
            "@typescript-eslint/no-unsafe-call": 0,
            "no-useless-escape": 0,
            "comma-dangle": [
                "warn",
                "never"
            ],
            "no-console": "warn",
            "no-unused-vars": [
                "warn",
                {
                    "args": "none"
                }
            ],
            "vue/no-unused-components": "warn",
            "array-bracket-newline": [
                "warn",
                {
                    "multiline": true,
                    "minItems": 2
                }
            ],
            "array-element-newline": [
                "warn",
                "always"
            ],
            "quotes": [
                "warn",
                "double",
                {
                    "avoidEscape": true
                }
            ],
            "indent": [
                "warn",
                4,
                {
                    "SwitchCase": 1
                }
            ],
            "semi": [
                "warn",
                "always"
            ],
            "semi-style": [
                "error",
                "last"
            ],
            "vue/multi-word-component-names": 0,
            "vue/script-indent": [
                "warn",
                4,
                {
                    "baseIndent": 0,
                    "switchCase": 1,
                    "ignores": []
                }
            ],
            "vue/html-indent": [
                "warn",
                4,
                {
                    "attribute": 1,
                    "baseIndent": 1,
                    "closeBracket": 0,
                    "alignAttributesVertically": true,
                    "ignores": []
                }
            ],
            "vue/html-closing-bracket-newline": [
                "warn",
                {
                    "singleline": "never",
                    "multiline": "never"
                }
            ],
            "vue/html-self-closing": [
                "warn",
                {
                    "html": {
                        "void": "any",
                        "normal": "always",
                        "component": "always"
                    },
                    "svg": "always",
                    "math": "always"
                }
            ],
            "vue/no-v-html": 0,
            "vue/script-setup-uses-vars": 0,
            "vue/component-definition-name-casing": 0,
            "vue/custom-event-name-casing": 0,
            "vue/no-lone-template": 0
        }
    }
];
