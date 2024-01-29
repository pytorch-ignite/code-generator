<template>
  <button
    aria-label="Toggle Color Scheme"
    @click="toggleTheme"
    title="Toggle Light/Dark mode"
    class="sun-moon-btn"
    id="toggleDark"
  >
    <svg
      id="sun"
      xmlns="http://www.w3.org/2000/svg"
      class="h-6 w-6"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
      />
    </svg>

    <svg
      id="moon"
      xmlns="http://www.w3.org/2000/svg"
      class="h-6 w-6 hidden"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
      />
    </svg>
  </button>
</template>

<style scoped>
@import url('./css/nav-right.css');

*,
::before,
::after {
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  border-width: 0;
  border-style: solid;
  border-color: #e5e7eb;
}

* {
  --tw-ring-inset: var(--tw-empty, /*!*/ /*!*/);
  --tw-ring-offset-width: 0px;
  --tw-ring-offset-color: #fff;
  --tw-ring-color: rgba(59, 130, 246, 0.5);
  --tw-ring-offset-shadow: 0 0 #0000;
  --tw-ring-shadow: 0 0 #0000;
  --tw-shadow: 0 0 #0000;
}

:root {
  -moz-tab-size: 4;
  -o-tab-size: 4;
  tab-size: 4;
}

:-moz-focusring {
  outline: 1px dotted ButtonText;
}

:-moz-ui-invalid {
  box-shadow: none;
}

::moz-focus-inner {
  border-style: none;
  padding: 0;
}

::-webkit-inner-spin-button,
::-webkit-outer-spin-button {
  height: auto;
}

::-webkit-search-decoration {
  -webkit-appearance: none;
}

::-webkit-file-upload-button {
  -webkit-appearance: button;
  font: inherit;
}

[type='search'] {
  -webkit-appearance: textfield;
  outline-offset: -2px;
}

abbr[title] {
  -webkit-text-decoration: underline dotted;
  text-decoration: underline dotted;
}

a {
  color: inherit;
  text-decoration: inherit;
}

body {
  margin: 0;
  font-family: inherit;
  line-height: inherit;
}

button {
  font-family: inherit;
  font-size: 100%;
  line-height: 1.15;
  margin: 0;
  text-transform: none;
  background-color: transparent;
  background-image: none;
  padding: 0;
  line-height: inherit;
  color: inherit;
}

button,
[type='button'],
[type='reset'],
[type='submit'] {
  -webkit-appearance: button;
}

button,
[role='button'] {
  cursor: pointer;
}

code {
  font-size: 1em;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
    'Liberation Mono', 'Courier New', monospace;
}

html {
  -webkit-text-size-adjust: 100%;
  font-family: Inter var, Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans',
    sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
    'Noto Color Emoji';
  line-height: 1.5;
}

h1,
p {
  margin: 0;
}

h1 {
  font-size: inherit;
  font-weight: inherit;
  margin: 0;
}

h1,
h2,
p {
  margin: 0;
}

h1,
h2 {
  font-size: inherit;
  font-weight: inherit;
}

h2 {
  margin: 0;
  font-size: inherit;
  font-weight: inherit;
}

h2,
p {
  margin: 0;
}

h5 {
  margin: 0;
  font-size: inherit;
  font-weight: inherit;
}

img {
  border-style: solid;
  display: block;
  vertical-align: middle;
  max-width: 100%;
  height: auto;
}

p {
  margin: 0;
}

summary {
  display: list-item;
}

svg {
  display: block;
  vertical-align: middle;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.prose {
  color: #374151;
  max-width: none;
  font-size: 1rem;
  line-height: 1.75;
}

.prose [class~='lead'] {
  color: #4b5563;
  font-size: 1.25em;
  line-height: 1.6;
  margin-top: 1.2em;
  margin-bottom: 1.2em;
}

.prose a {
  color: #111827;
  text-decoration: none;
  font-weight: 500;
}

.prose a:hover {
  text-decoration: underline;
}

.prose strong {
  color: #111827;
  font-weight: 600;
}

.prose ol[type='A'] {
  --list-counter-style: upper-alpha;
}

.prose ol[type='a'] {
  --list-counter-style: lower-alpha;
}

.prose ol[type='A s'] {
  --list-counter-style: upper-alpha;
}

.prose ol[type='a s'] {
  --list-counter-style: lower-alpha;
}

.prose ol[type='I'] {
  --list-counter-style: upper-roman;
}

.prose ol[type='i'] {
  --list-counter-style: lower-roman;
}

.prose ol[type='I s'] {
  --list-counter-style: upper-roman;
}

.prose ol[type='i s'] {
  --list-counter-style: lower-roman;
}

.prose ol[type='1'] {
  --list-counter-style: decimal;
}

.prose ol > li {
  position: relative;
  padding-left: 1.75em;
}

.prose ol > li::before {
  content: counter(list-item, var(--list-counter-style, decimal)) '.';
  position: absolute;
  font-weight: 400;
  color: #6b7280;
  left: 0;
}

.prose ul > li {
  position: relative;
  padding-left: 1.75em;
}

.prose ul > li::before {
  content: '';
  position: absolute;
  background-color: #d1d5db;
  border-radius: 50%;
  width: 0.375em;
  height: 0.375em;
  top: calc(0.875em - 0.1875em);
  left: 0.25em;
}

.prose hr {
  border-color: #e5e7eb;
  margin-top: 3em;
  margin-bottom: 3em;
}

.prose blockquote {
  font-weight: 500;
  font-style: italic;
  color: #111827;
  border-left-width: 0.25rem;
  border-color: #e5e7eb;
  quotes: '\201C''\201D''\2018''\2019';
  margin-top: 1.6em;
  margin-bottom: 1.6em;
  padding-left: 1em;
}

.prose blockquote p:first-of-type::before {
  content: open-quote;
}

.prose blockquote p:last-of-type::after {
  content: close-quote;
}

.prose h1 {
  color: #111827;
  font-weight: 800;
  font-size: 2.25em;
  margin-top: 0;
  margin-bottom: 0.8888889em;
  line-height: 1.1111111;
}

.prose h2 {
  color: #111827;
  font-weight: 700;
  font-size: 1.5em;
  margin-top: 2em;
  margin-bottom: 1em;
  line-height: 1.3333333;
}

.prose h3 {
  color: #111827;
  font-weight: 600;
  font-size: 1.25em;
  margin-top: 1.6em;
  margin-bottom: 0.6em;
  line-height: 1.6;
}

.prose h4 {
  color: #111827;
  font-weight: 600;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  line-height: 1.5;
}

.prose figure figcaption {
  color: #6b7280;
  font-size: 0.875em;
  line-height: 1.4285714;
  margin-top: 0.8571429em;
}

.prose code {
  color: #8b5cf6;
  font-weight: 600;
  font-size: 0.875em;
}

.prose code::before {
  content: '`';
}

.prose code::after {
  content: '`';
}

.prose a code {
  color: #111827;
}

.prose pre {
  color: #e5e7eb;
  background-color: #1f2937;
  overflow-x: auto;
  font-size: 0.875em;
  line-height: 1.7142857;
  margin-top: 1.7142857em;
  margin-bottom: 1.7142857em;
  border-radius: 0.375rem;
  padding-top: 0.8571429em;
  padding-right: 1.1428571em;
  padding-bottom: 0.8571429em;
  padding-left: 1.1428571em;
}

.prose pre code {
  background-color: transparent;
  border-width: 0;
  border-radius: 0;
  padding: 0;
  font-weight: 400;
  color: inherit;
  font-size: inherit;
  font-family: inherit;
  line-height: inherit;
}

.prose pre code::before {
  content: none;
}

.prose pre code::after {
  content: none;
}

.prose table {
  width: 100%;
  table-layout: auto;
  text-align: left;
  margin-top: 2em;
  margin-bottom: 2em;
  font-size: 0.875em;
  line-height: 1.7142857;
}

.prose thead {
  color: #111827;
  font-weight: 600;
  border-bottom-width: 1px;
  border-bottom-color: #d1d5db;
}

.prose thead th {
  vertical-align: bottom;
  padding-right: 0.5714286em;
  padding-bottom: 0.5714286em;
  padding-left: 0.5714286em;
}

.prose tbody tr {
  border-bottom-width: 1px;
  border-bottom-color: #e5e7eb;
}

.prose tbody tr:last-child {
  border-bottom-width: 0;
}

.prose tbody td {
  vertical-align: top;
  padding-top: 0.5714286em;
  padding-right: 0.5714286em;
  padding-bottom: 0.5714286em;
  padding-left: 0.5714286em;
}

.prose p {
  margin-top: 1.25em;
  margin-bottom: 1.25em;
}

.prose img {
  margin-top: 2em;
  margin-bottom: 2em;
}

.prose video {
  margin-top: 2em;
  margin-bottom: 2em;
}

.prose figure {
  margin-top: 2em;
  margin-bottom: 2em;
}

.prose figure > * {
  margin-top: 0;
  margin-bottom: 0;
}

.prose h2 code {
  font-size: 0.875em;
}

.prose h3 code {
  font-size: 0.9em;
}

.prose ol {
  margin-top: 1.25em;
  margin-bottom: 1.25em;
  list-style-type: none;
}

.prose ul {
  margin-top: 1.25em;
  margin-bottom: 1.25em;
  list-style-type: none;
}

.prose li {
  margin-top: 0.5em;
  margin-bottom: 0.5em;
}

.prose > ul > li p {
  margin-top: 0.75em;
  margin-bottom: 0.75em;
}

.prose > ul > li > *:first-child {
  margin-top: 1.25em;
}

.prose > ul > li > *:last-child {
  margin-bottom: 1.25em;
}

.prose > ol > li > *:first-child {
  margin-top: 1.25em;
}

.prose > ol > li > *:last-child {
  margin-bottom: 1.25em;
}

.prose ul ul,
.prose ul ol,
.prose ol ul,
.prose ol ol {
  margin-top: 0.75em;
  margin-bottom: 0.75em;
}

.prose hr + * {
  margin-top: 0;
}

.prose h2 + * {
  margin-top: 0;
}

.prose h3 + * {
  margin-top: 0;
}

.prose h4 + * {
  margin-top: 0;
}

.prose thead th:first-child {
  padding-left: 0;
}

.prose thead th:last-child {
  padding-right: 0;
}

.prose tbody td:first-child {
  padding-left: 0;
}

.prose tbody td:last-child {
  padding-right: 0;
}

.prose > :first-child {
  margin-top: 0;
}

.prose > :last-child {
  margin-bottom: 0;
}

.dark .prose {
  color: #d6d3d1;
}

.dark .prose [class~='lead'] {
  color: #e7e5e4;
}

.dark .prose a {
  color: #e7e5e4;
}

.dark .prose strong {
  color: #e7e5e4;
}

.dark .prose ol > li::before {
  color: #78716c;
}

.dark .prose ul > li::before {
  background-color: #78716c;
}

.dark .prose hr {
  border-color: #292524;
}

.dark .prose blockquote {
  color: #78716c;
  border-color: #44403c;
}

.dark .prose h1 {
  color: #e7e5e4;
}

.dark .prose h2 {
  color: #e7e5e4;
}

.dark .prose h3 {
  color: #e7e5e4;
}

.dark .prose h4 {
  color: #e7e5e4;
}

.dark .prose figure figcaption {
  color: #a8a29e;
}

.dark .prose code {
  color: #d6d3d1;
}

.dark .prose a code {
  color: #f5f5f4;
}

.dark .prose pre {
  color: #f5f5f4;
  background-color: #1c1917;
}

.dark .prose pre code {
  background-color: transparent;
  color: inherit;
}

.dark .prose thead {
  color: #f5f5f4;
  border-bottom-color: #44403c;
}

.dark .prose tbody tr {
  border-bottom-color: #292524;
}

.prose-red a {
  color: #dc2626;
}

.prose-red a code {
  color: #dc2626;
}

.divide-y > :not([hidden]) ~ :not([hidden]) {
  --tw-divide-y-reverse: 0;
  border-top-width: calc(1px * calc(1 - var(--tw-divide-y-reverse)));
  border-bottom-width: calc(1px * var(--tw-divide-y-reverse));
}

.dark .dark\:divide-dark-200 > :not([hidden]) ~ :not([hidden]) {
  --tw-divide-opacity: 1;
  border-color: rgba(50, 50, 50, var(--tw-divide-opacity));
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.dark .dark\:bg-clip-text {
  -webkit-background-clip: text;
  background-clip: text;
}

.bg-gray-200 {
  --tw-bg-opacity: 1;
  background-color: rgba(229, 231, 235, var(--tw-bg-opacity));
}

.dark .dark\:bg-dark-200 {
  --tw-bg-opacity: 1;
  background-color: rgba(50, 50, 50, var(--tw-bg-opacity));
}

.bg-\$c-primary {
  background-color: var(--c-primary);
}

.hover\:bg-\$c-primary:hover {
  background-color: var(--c-primary);
}

.bg-white {
  --tw-bg-opacity: 1;
  background-color: rgba(255, 255, 255, var(--tw-bg-opacity));
}

.dark .dark\:bg-dark-700 {
  --tw-bg-opacity: 1;
  background-color: rgba(27, 27, 27, var(--tw-bg-opacity));
}

.bg-red-100 {
  --tw-bg-opacity: 1;
  background-color: rgba(254, 226, 226, var(--tw-bg-opacity));
}

.dark .dark\:bg-dark-400 {
  --tw-bg-opacity: 1;
  background-color: rgba(34, 34, 34, var(--tw-bg-opacity));
}

.bg-green-100 {
  --tw-bg-opacity: 1;
  background-color: rgba(209, 250, 229, var(--tw-bg-opacity));
}

.bg-yellow-100 {
  --tw-bg-opacity: 1;
  background-color: rgba(254, 243, 199, var(--tw-bg-opacity));
}

.bg-blue-100 {
  --tw-bg-opacity: 1;
  background-color: rgba(219, 234, 254, var(--tw-bg-opacity));
}

.children\:hover\:bg-gray-200:hover > * {
  --tw-bg-opacity: 1;
  background-color: rgba(229, 231, 235, var(--tw-bg-opacity));
}

.dark .dark\:children\:hover\:bg-dark-200:hover > * {
  --tw-bg-opacity: 1;
  background-color: rgba(50, 50, 50, var(--tw-bg-opacity));
}

.bg-gradient-to-br {
  background-image: -o-linear-gradient(top left, var(--tw-gradient-stops));
  background-image: -webkit-gradient(
    linear,
    left top,
    right bottom,
    from(var(--tw-gradient-stops))
  );
  background-image: linear-gradient(to bottom right, var(--tw-gradient-stops));
}

.dark .dark\:from-red-500 {
  --tw-gradient-from: rgba(239, 68, 68, var(--tw-from-opacity, 1));
  --tw-gradient-stops: var(--tw-gradient-from),
    var(--tw-gradient-to, rgba(255, 255, 255, 0));
}

.dark .dark\:to-amber-400 {
  --tw-gradient-to: rgba(251, 191, 36, var(--tw-to-opacity, 1));
}

.dark .dark\:border-dark-200 {
  --tw-border-opacity: 1;
  border-color: rgba(50, 50, 50, var(--tw-border-opacity));
}

.border-\$c-primary {
  border-color: var(--c-primary);
}

.border-red-500 {
  --tw-border-opacity: 1;
  border-color: rgba(239, 68, 68, var(--tw-border-opacity));
}

.border-green-500 {
  --tw-border-opacity: 1;
  border-color: rgba(16, 185, 129, var(--tw-border-opacity));
}

.border-yellow-500 {
  --tw-border-opacity: 1;
  border-color: rgba(245, 158, 11, var(--tw-border-opacity));
}

.border-blue-500 {
  --tw-border-opacity: 1;
  border-color: rgba(59, 130, 246, var(--tw-border-opacity));
}

.dark .dark\:border-b-dark-200 {
  --tw-border-opacity: 1;
  border-bottom-color: rgba(50, 50, 50, var(--tw-border-opacity));
}

.rounded-lg {
  border-radius: 0.5rem;
}

.children\:rounded-lg > * {
  border-radius: 0.5rem;
}

.border {
  border-width: 1px;
}

.border-t {
  border-top-width: 1px;
}

.border-b {
  border-bottom-width: 1px;
}

.\!block {
  display: block !important;
}

.block {
  display: block;
}

.inline-block {
  display: inline-block;
}

.flex {
  display: -webkit-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;
}

.grid {
  display: -ms-grid;
  display: grid;
}

.hidden {
  display: none;
}

.before\:hidden::before {
  display: none;
}

.flex-wrap {
  -ms-flex-wrap: wrap;
  -webkit-flex-wrap: wrap;
  flex-wrap: wrap;
}

.place-items-center {
  place-items: center;
}

.place-content-center {
  place-content: center;
}

.place-self-start {
  -ms-grid-row-align: start;
  -ms-grid-column-align: start;
  place-self: start;
}

.items-center {
  -webkit-box-align: center;
  -ms-flex-align: center;
  -webkit-align-items: center;
  align-items: center;
}

.justify-items-center {
  justify-items: center;
}

.justify-center {
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  -webkit-justify-content: center;
  justify-content: center;
}

.justify-between {
  -webkit-box-pack: justify;
  -ms-flex-pack: justify;
  -webkit-justify-content: space-between;
  justify-content: space-between;
}

.flex-grow {
  -webkit-box-flex: 1;
  -ms-flex-positive: 1;
  -webkit-flex-grow: 1;
  flex-grow: 1;
}

.float-right {
  float: right;
}

.font-sans {
  font-family: Inter var, Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans',
    sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
    'Noto Color Emoji';
}

.font-semibold {
  font-weight: 600;
}

.font-light {
  font-weight: 300;
}

.h-full {
  height: 100%;
}

.h-5 {
  height: 1.25rem;
}

.h-6 {
  height: 1.5rem;
}

.h-\$header-height {
  height: var(--header-height);
}

.h-40px {
  height: 40px;
}

.h-\$aside-height {
  height: var(--aside-height);
}

.text-2xl {
  font-size: 1.5rem;
  line-height: 2rem;
}

.text-xl {
  font-size: 1.25rem;
  line-height: 1.75rem;
}

.text-sm {
  font-size: 0.875rem;
  line-height: 1.25rem;
}

.m-4 {
  margin: 1rem;
}

.mx-auto {
  margin-left: auto;
  margin-right: auto;
}

.my-4 {
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.mx-2 {
  margin-left: 0.5rem;
  margin-right: 0.5rem;
}

.my-1 {
  margin-top: 0.25rem;
  margin-bottom: 0.25rem;
}

.mr-1 {
  margin-right: 0.25rem;
}

.\!mt-2 {
  margin-top: 0.5rem !important;
}

.ml-1 {
  margin-left: 0.25rem;
}

.max-w-6xl {
  max-width: 72rem;
}

.max-w-4xl {
  max-width: 56rem;
}

.min-w-0 {
  min-width: 0px;
}

.min-w-50 {
  min-width: 12.5rem;
}

.overflow-hidden {
  overflow: hidden;
}

.overflow-x-auto {
  overflow-x: auto;
}

.overflow-y-auto {
  overflow-y: auto;
}

.p-4 {
  padding: 1rem;
}

.p-1 {
  padding: 0.25rem;
}

.p-2 {
  padding: 0.5rem;
}

.py-6 {
  padding-top: 1.5rem;
  padding-bottom: 1.5rem;
}

.px-6 {
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
}

.py-3 {
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
}

.py-2 {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.py-1 {
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
}

.px-2 {
  padding-left: 0.5rem;
  padding-right: 0.5rem;
}

.px-1 {
  padding-left: 0.25rem;
  padding-right: 0.25rem;
}

.pb-4 {
  padding-bottom: 1rem;
}

.\!pl-0 {
  padding-left: 0px !important;
}

.pb-2 {
  padding-bottom: 0.5rem;
}

.fixed {
  position: fixed;
}

.absolute {
  position: absolute;
}

.relative {
  position: relative;
}

.sticky {
  position: -webkit-sticky;
  position: sticky;
}

.top-0 {
  top: 0px;
}

.right-0 {
  right: 0px;
}

.left-0 {
  left: 0px;
}

.top-\$header-height {
  top: var(--header-height);
}

.top-1 {
  top: 0.25rem;
}

.right-1 {
  right: 0.25rem;
}

.hover\:shadow-xl:hover {
  --tw-shadow: 0 20px 25px -5px rgb(0 0 0/0.1), 0 8px 10px -6px rgb(0 0 0/0.1);
  --tw-shadow-colored: 0 20px 25px -5px var(--tw-shadow-color),
    0 8px 10px -6px var(--tw-shadow-color);
  -webkit-box-shadow: var(--tw-ring-offset-shadow, 0 0 #0000),
    var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow);
  box-shadow: var(--tw-ring-offset-shadow, 0 0 #0000),
    var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow);
}

.dark .dark\:shadow-red-500 {
  --tw-shadow-color: rgba(239, 68, 68, 1);
  --tw-shadow: var(--tw-shadow-colored);
}

.dark .dark\:shadow-green-500 {
  --tw-shadow-color: rgba(16, 185, 129, 1);
  --tw-shadow: var(--tw-shadow-colored);
}

.dark .dark\:shadow-yellow-500 {
  --tw-shadow-color: rgba(245, 158, 11, 1);
  --tw-shadow: var(--tw-shadow-colored);
}

.dark .dark\:shadow-blue-500 {
  --tw-shadow-color: rgba(59, 130, 246, 1);
  --tw-shadow: var(--tw-shadow-colored);
}

.text-center {
  text-align: center;
}

.dark .dark\:text-transparent {
  color: transparent;
}

.text-white {
  --tw-text-opacity: 1;
  color: rgba(255, 255, 255, var(--tw-text-opacity));
}

.text-blue-gray-400 {
  --tw-text-opacity: 1;
  color: rgba(148, 163, 184, var(--tw-text-opacity));
}

.group:hover .group-hover\:text-\$c-primary {
  color: var(--c-primary);
}

.hover\:text-white:hover {
  --tw-text-opacity: 1;
  color: rgba(255, 255, 255, var(--tw-text-opacity));
}

.hover\:text-blue-gray-500:hover {
  --tw-text-opacity: 1;
  color: rgba(100, 116, 139, var(--tw-text-opacity));
}

.text-blue-gray-600 {
  --tw-text-opacity: 1;
  color: rgba(71, 85, 105, var(--tw-text-opacity));
}

.dark .dark\:text-warm-gray-200 {
  --tw-text-opacity: 1;
  color: rgba(231, 229, 228, var(--tw-text-opacity));
}

.hover\:text-\$c-primary:hover {
  color: var(--c-primary);
}

.uppercase {
  text-transform: uppercase;
}

.hover\:underline:hover {
  -webkit-text-decoration-line: underline;
  text-decoration-line: underline;
}

.antialiased {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.align-middle {
  vertical-align: middle;
}

.whitespace-nowrap {
  white-space: nowrap;
}

.children\:break-all > * {
  word-break: break-all;
}

.w-4\/5 {
  width: 80%;
}

.w-auto {
  width: auto;
}

.w-5 {
  width: 1.25rem;
}

.w-6 {
  width: 1.5rem;
}

.w-max {
  width: -webkit-max-content;
  width: -moz-max-content;
  width: max-content;
}

.z-10 {
  z-index: 10;
}

.gap-4 {
  grid-gap: 1rem;
  gap: 1rem;
}

.gap-x-12 {
  -webkit-column-gap: 3rem;
  -moz-column-gap: 3rem;
  grid-column-gap: 3rem;
  column-gap: 3rem;
}

.gap-x-4 {
  -webkit-column-gap: 1rem;
  -moz-column-gap: 1rem;
  grid-column-gap: 1rem;
  column-gap: 1rem;
}

.gap-y-4 {
  -webkit-row-gap: 1rem;
  -moz-row-gap: 1rem;
  grid-row-gap: 1rem;
  row-gap: 1rem;
}

.gap-y-6 {
  -webkit-row-gap: 1.5rem;
  -moz-row-gap: 1.5rem;
  grid-row-gap: 1.5rem;
  row-gap: 1.5rem;
}

.grid-cols-\[1fr\2c 2fr\2c 1fr\] {
  grid-template-columns: 1fr 2fr 1fr;
}

.grid-cols-1 {
  grid-template-columns: repeat(1, minmax(0, 1fr));
}

.grid-cols-\[1fr\2c 3fr\] {
  grid-template-columns: 1fr 3fr;
}

.grid-cols-2 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.transform {
  --tw-translate-x: 0;
  --tw-translate-y: 0;
  --tw-translate-z: 0;
  --tw-rotate: 0;
  --tw-rotate-x: 0;
  --tw-rotate-y: 0;
  --tw-rotate-z: 0;
  --tw-skew-x: 0;
  --tw-skew-y: 0;
  --tw-scale-x: 1;
  --tw-scale-y: 1;
  --tw-scale-z: 1;
  -webkit-transform: translateX(var(--tw-translate-x))
    translateY(var(--tw-translate-y)) translateZ(var(--tw-translate-z))
    rotate(var(--tw-rotate)) rotateX(var(--tw-rotate-x))
    rotateY(var(--tw-rotate-y)) rotateZ(var(--tw-rotate-z))
    skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x))
    scaleY(var(--tw-scale-y)) scaleZ(var(--tw-scale-z));
  -ms-transform: translateX(var(--tw-translate-x))
    translateY(var(--tw-translate-y)) translateZ(var(--tw-translate-z))
    rotate(var(--tw-rotate)) rotateX(var(--tw-rotate-x))
    rotateY(var(--tw-rotate-y)) rotateZ(var(--tw-rotate-z))
    skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x))
    scaleY(var(--tw-scale-y)) scaleZ(var(--tw-scale-z));
  transform: translateX(var(--tw-translate-x)) translateY(var(--tw-translate-y))
    translateZ(var(--tw-translate-z)) rotate(var(--tw-rotate))
    rotateX(var(--tw-rotate-x)) rotateY(var(--tw-rotate-y))
    rotateZ(var(--tw-rotate-z)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y))
    scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))
    scaleZ(var(--tw-scale-z));
}

.group:hover .group-hover\:transform {
  --tw-translate-x: 0;
  --tw-translate-y: 0;
  --tw-translate-z: 0;
  --tw-rotate: 0;
  --tw-rotate-x: 0;
  --tw-rotate-y: 0;
  --tw-rotate-z: 0;
  --tw-skew-x: 0;
  --tw-skew-y: 0;
  --tw-scale-x: 1;
  --tw-scale-y: 1;
  --tw-scale-z: 1;
  -webkit-transform: translateX(var(--tw-translate-x))
    translateY(var(--tw-translate-y)) translateZ(var(--tw-translate-z))
    rotate(var(--tw-rotate)) rotateX(var(--tw-rotate-x))
    rotateY(var(--tw-rotate-y)) rotateZ(var(--tw-rotate-z))
    skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x))
    scaleY(var(--tw-scale-y)) scaleZ(var(--tw-scale-z));
  -ms-transform: translateX(var(--tw-translate-x))
    translateY(var(--tw-translate-y)) translateZ(var(--tw-translate-z))
    rotate(var(--tw-rotate)) rotateX(var(--tw-rotate-x))
    rotateY(var(--tw-rotate-y)) rotateZ(var(--tw-rotate-z))
    skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x))
    scaleY(var(--tw-scale-y)) scaleZ(var(--tw-scale-z));
  transform: translateX(var(--tw-translate-x)) translateY(var(--tw-translate-y))
    translateZ(var(--tw-translate-z)) rotate(var(--tw-rotate))
    rotateX(var(--tw-rotate-x)) rotateY(var(--tw-rotate-y))
    rotateZ(var(--tw-rotate-z)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y))
    scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))
    scaleZ(var(--tw-scale-z));
}

.rotate-90 {
  --tw-rotate: 90deg;
}

.group:hover .group-hover\:translate-x-1 {
  --tw-translate-x: 0.25rem;
}

.group:hover .group-hover\:-translate-x-1 {
  --tw-translate-x: -0.25rem;
}

.transition-shadow {
  -webkit-transition-property: -webkit-box-shadow;
  -o-transition-property: box-shadow;
  transition-property: box-shadow, -webkit-box-shadow;
  -webkit-transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  -o-transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  -webkit-transition-duration: 150ms;
  -o-transition-duration: 150ms;
  transition-duration: 150ms;
}

.transition-transform {
  -webkit-transition-property: -webkit-transform;
  -o-transition-property: transform;
  transition-property: transform, -webkit-transform;
  -webkit-transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  -o-transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  -webkit-transition-duration: 150ms;
  -o-transition-duration: 150ms;
  transition-duration: 150ms;
}

.duration-300 {
  -webkit-transition-duration: 300ms;
  -o-transition-duration: 300ms;
  transition-duration: 300ms;
}

@media (min-width: 640px) {
  .sm\:grid-cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .sm\:grid-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .sm\:col-start-2 {
    grid-column-start: 2;
  }

  .sm\:row-span-2 {
    -ms-grid-row-span: span 2 / span 2;
    grid-row: span 2 / span 2;
  }
}

@media (min-width: 1024px) {
  .lg\:block {
    display: block;
  }

  .group:hover .lg\:group-hover\:block {
    display: block;
  }

  .lg\:flex {
    display: -webkit-box;
    display: -ms-flexbox;
    display: -webkit-flex;
    display: flex;
  }

  .lg\:grid {
    display: -ms-grid;
    display: grid;
  }

  .lg\:hidden {
    display: none;
  }

  .lg\:text-3xl {
    font-size: 1.875rem;
    line-height: 2.25rem;
  }

  .lg\:text-xl {
    font-size: 1.25rem;
    line-height: 1.75rem;
  }

  .lg\:text-2xl {
    font-size: 1.5rem;
    line-height: 2rem;
  }

  .lg\:p-2 {
    padding: 0.5rem;
  }

  .lg\:absolute {
    position: absolute;
  }

  .lg\:sticky {
    position: -webkit-sticky;
    position: sticky;
  }

  .lg\:w-3\/5 {
    width: 60%;
  }

  .lg\:grid-flow-row-dense {
    grid-auto-flow: row dense;
  }

  .lg\:grid-cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .lg\:grid-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .lg\:col-span-1 {
    -ms-grid-column-span: span 1 / span 1;
    grid-column: span 1 / span 1;
  }

  .lg\:col-start-2 {
    grid-column-start: 2;
  }

  .lg\:col-start-1 {
    grid-column-start: 1;
  }
}

@media (min-width: 1280px) {
  .xl\:grid-cols-\[1fr\2c 3fr\2c 1fr\] {
    grid-template-columns: 1fr 3fr 1fr;
  }
}

@media (max-width: 1023.9px) {
  .\<lg\:border-r {
    border-right-width: 1px;
  }

  .\<lg\:hidden {
    display: none;
  }

  .\<lg\:w-75 {
    width: 18.75rem;
  }

  .\<lg\:-translate-x-full {
    --tw-translate-x: -100%;
  }
}

@media (max-width: 639.9px) {
  .\<sm\:px-4 {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>

<script>
export default {
  mounted() {
    const initUserTheme = this.getTheme() || this.getMediaPreference()
    this.setTheme(initUserTheme)
  },

  data() {
    return {
      userTheme: 'light-theme'
    }
  },

  methods: {
    toggleTheme() {
      const sun = document.getElementById('sun')
      const moon = document.getElementById('moon')
      const activeTheme = localStorage.getItem('user-theme')
      if (activeTheme === 'light-theme') {
        this.setTheme('dark-theme')
        this.toggleClassList()
      } else {
        this.setTheme('light-theme')
        this.toggleClassList()
      }
    },

    getTheme() {
      return localStorage.getItem('user-theme')
    },

    setTheme(theme) {
      localStorage.setItem('user-theme', theme)
      this.userTheme = theme
      document.documentElement.className = theme
    },

    toggleClassList() {
      sun.classList.toggle('hidden')
      moon.classList.toggle('hidden')
    },

    getMediaPreference() {
      const hasDarkPreference = window.matchMedia(
        '(prefers-color-scheme: dark)'
      ).matches
      if (hasDarkPreference) {
        return 'dark-theme'
      } else {
        return 'light-theme'
      }
    }
  }
}
</script>
