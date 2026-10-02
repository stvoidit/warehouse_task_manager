import stylistic from "@stylistic/eslint-plugin";
import pluginVue from "eslint-plugin-vue";
import { defineConfig } from "eslint/config";
import globals from "globals";
import tseslint from "typescript-eslint";
import vueEslintParser from "vue-eslint-parser";

export default defineConfig(
    stylistic.configs.customize({
        commaDangle: "always-multiline",
        quotes: "double",
        semi: true,
        indent: 4,
        jsx: false,
    }),
    stylistic.configs["disable-legacy"],
    tseslint.configs.stylisticTypeChecked,
    tseslint.configs.strictTypeChecked,
    pluginVue.configs["flat/recommended"],
    {
        languageOptions: {
            globals: {
                ...globals.browser,
                ...globals.es2025,
            },
            parser: vueEslintParser,
            parserOptions: {
                parser: tseslint.parser,
                ecmaVersion: "latest",
                sourceType: "module",
                projectService: true,
                tsconfigRootDir: import.meta.dirname,
                extraFileExtensions: [ ".vue" ],
            },
        },
        plugins: {
            "@stylistic": stylistic,
            "@typescript-eslint": tseslint.plugin,
        },
        rules: {
            "@stylistic/quotes": [ "error",
                "double",
                {
                    allowTemplateLiterals: "always",
                },
            ],
            "@stylistic/array-bracket-spacing": [ "error", "always" ],
            "@stylistic/array-element-newline": [ "error",
                {
                    consistent: true,
                    multiline: true,
                },
            ],
            "@stylistic/block-spacing": [ "error", "always" ],
            "@stylistic/brace-style": [
                "error",
                "1tbs",
                {
                    allowSingleLine: false,
                },
            ],
            "@typescript-eslint/ban-ts-comment": 0,
            "@typescript-eslint/no-non-null-assertion": 0,
            "@typescript-eslint/no-misused-spread": 0,
            "@typescript-eslint/no-dynamic-delete": 0,
            "@typescript-eslint/no-unnecessary-condition": "warn",
            "@typescript-eslint/no-empty-function": "warn",
            "@typescript-eslint/no-explicit-any": [
                "error",
                {
                    fixToUnknown: true,
                    ignoreRestArgs: true,
                },
            ],
            // "@typescript-eslint/no-confusing-void-expression": ["warn", {
            //     ignoreArrowShorthand: true,
            //     ignoreVoidOperator: true,
            //     ignoreVoidReturningFunctions: true,
            // }]
            "@typescript-eslint/no-unsafe-assignment": 0,
            "@typescript-eslint/no-unsafe-member-access": 0,
            "@typescript-eslint/no-unsafe-call": 0,
            "@typescript-eslint/use-unknown-in-catch-callback-variable": "error",
            "@typescript-eslint/prefer-nullish-coalescing": [
                "warn",
                {
                    ignoreTernaryTests: true,
                    ignorePrimitives: true,
                },
            ],
            "@typescript-eslint/restrict-template-expressions": [
                "warn",
                {
                    allowNumber: true,
                    allowNever: true,
                },
            ],
            "@typescript-eslint/no-unused-vars": [
                "warn",
                {
                    varsIgnorePattern: "^_",
                    args: "after-used",
                    argsIgnorePattern: "^_",
                    destructuredArrayIgnorePattern: "^_",
                    caughtErrors: "none",
                },
            ],
            "@typescript-eslint/no-unsafe-return": "warn",
            "@typescript-eslint/no-unsafe-argument": "warn",
            "@typescript-eslint/no-floating-promises": [ "warn",
                {
                    ignoreIIFE: true,
                    ignoreVoid: true,
                    checkThenables: false,
                },
            ],
            "vue/component-definition-name-casing": 0,
            "vue/html-closing-bracket-newline": [
                "error",
                {
                    singleline: "never",
                    multiline: "never",
                },
            ],
            "vue/html-indent": [
                "error",
                4,
                {
                    alignAttributesVertically: true,
                    attribute: 1,
                    baseIndent: 1,
                    closeBracket: 0,
                },
            ],
            "vue/no-unused-components": "error",
            "vue/no-v-html": 0,
            "vue/script-indent": [
                "error",
                4,
                {
                    baseIndent: 0,
                    ignores: [],
                    switchCase: 1,
                },
            ],
        },
    },
    {
        ignores: [
            "dist",
            "public",
            "node_modules",
        ],
    },
);
