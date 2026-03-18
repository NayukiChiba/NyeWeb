<template>
  <article class="markdown-body" ref="containerRef">
    <div v-html="renderedHtml"></div>
  </article>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import mermaid from 'mermaid'

// Markdown-it and plugins
import markdownit from 'markdown-it'
import mdAnchor from 'markdown-it-anchor'
import slugify from 'slugify'
import mdKatex from '@iktakahiro/markdown-it-katex'
import hljs from 'highlight.js'
import mdTable from 'markdown-it-multimd-table'

// CSS imports
import 'highlight.js/styles/github.css'
import 'github-markdown-css/github-markdown.css'
import 'katex/dist/katex.min.css'

// 初始化 Mermaid
mermaid.initialize({ startOnLoad: false, theme: 'default' })

const props = defineProps({
  content: {
    type: String,
    default: ''
  },
  category: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['headings-extracted'])

const containerRef = ref(null)
const renderedHtml = ref('')

// Markdown-it 配置
const md = markdownit({
  html: true,
  linkify: true,
  typographer: true,
  tables: true,
  breaks: true,
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return '<pre class="hljs"><code>' +
            hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
            '</code></pre>'
      } catch (__) {
      }
    }
    return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>'
  }
}).use(mdKatex, {
  throwOnError: false,
  errorColor: '#cc0000',
  delimiters: [
    { left: '$$', right: '$$', display: true },
    { left: '$', right: '$', display: false },
    { left: '\\(', right: '\\)', display: false },
    { left: '\\[', right: '\\]', display: true }
  ]
})
    .use(mdAnchor, {
      permalink: true,
      level: [1, 2, 3, 4, 5, 6],
      slugify: s => {
        let slug = slugify(s, { lower: true, locale: 'zh' })
        if (!slug || slug.startsWith('-')) {
          slug = 'heading-' + Math.abs(Math.floor(Math.random() * 1000000))
        }
        return slug
      },
      permalinkSymbol: '',
      permalinkBefore: true,
      permalinkClass: 'header-anchor'
    })
    .use(mdTable, {
      multiline: true,
      rowspan: true,
      headerless: true
    })

// 自定义代码块渲染，支持 Mermaid
const defaultFenceRenderer = md.renderer.rules.fence
md.renderer.rules.fence = (tokens, idx, options, env, self) => {
  const token = tokens[idx]
  const language = token.info.trim().split(/\s+/)[0]
  if (language === 'mermaid') {
    return `<div class="mermaid">${token.content}</div>`
  }
  const rawCode = defaultFenceRenderer(tokens, idx, options, env, self)

  return `
    <div class="code-block-wrapper">
      <div class="code-block-header">
        <div class="mac-dots">
          <span class="dot red"></span>
          <span class="dot yellow"></span>
          <span class="dot green"></span>
        </div>
        <span class="language-name">${language}</span>
        <button class="copy-code-btn" title="复制">复制</button>
      </div>
      ${rawCode}
    </div>
  `
}

// 修复图片相对路径问题
const defaultImageRenderer = md.renderer.rules.image
md.renderer.rules.image = function (tokens, idx, options, env, self) {
  const token = tokens[idx]
  const src = token.attrGet('src')
  if (src && src.startsWith('./')) {
    const articlePath = env.articlePath || ''
    const basePath = articlePath ? `/articles/knowledge/${articlePath}` : '/articles/knowledge'
    token.attrSet('src', `${basePath}/${src.substring(2)}`)
  }
  return defaultImageRenderer(tokens, idx, options, env, self)
}

const setupCopyButtons = () => {
  if (!containerRef.value) return
  containerRef.value.querySelectorAll('.copy-code-btn').forEach(button => {
    button.addEventListener('click', () => {
      const wrapper = button.closest('.code-block-wrapper')
      const code = wrapper.querySelector('code')
      if (code) {
        navigator.clipboard.writeText(code.innerText).then(() => {
          button.textContent = '成功复制!'
          setTimeout(() => {
            button.textContent = '复制'
          }, 2000)
        }).catch(err => {
          console.error('复制失败: ', err)
          button.textContent = '失败'
        })
      }
    })
  })
}

const extractHeadings = () => {
  if (!containerRef.value) return
  const headingElements = containerRef.value.querySelectorAll('h1, h2, h3, h4, h5, h6')
  const extracted = []
  headingElements.forEach((element, index) => {
    let id = element.id
    if (!id || id.startsWith('-')) {
      id = 'heading-' + index
      element.id = id
    }
    extracted.push({
      level: parseInt(element.tagName.substring(1), 10),
      text: element.textContent.replace('¶', '').trim(),
      id: id
    })
  })
  emit('headings-extracted', extracted)
}

const renderContent = async () => {
  if (!props.content) {
    renderedHtml.value = ''
    return
  }
  const env = { articlePath: props.category }
  renderedHtml.value = md.render(props.content, env)

  await nextTick()
  extractHeadings()
  setupCopyButtons()
  // 渲染 Mermaid 图表
  if (containerRef.value) {
    const mermaidElements = containerRef.value.querySelectorAll('.mermaid')
    if (mermaidElements.length) {
      mermaid.init(undefined, mermaidElements)
    }
  }
}

watch(() => props.content, renderContent)
onMounted(renderContent)
</script>

<style scoped>
.markdown-body {
  padding: 2rem 2.5rem;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  border: 1px solid #e5e7eb;
  line-height: 1.85;
  color: #1e293b;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', sans-serif;
  font-size: 1rem;
  word-wrap: break-word;
  overflow-wrap: break-word;
  max-width: 100% !important;
}

/* ─── Headings ─── */
:deep(h1), :deep(h2), :deep(h3), :deep(h4), :deep(h5), :deep(h6) {
  margin-top: 1.8em;
  margin-bottom: 0.6em;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.35;
  position: relative;
}

:deep(h1) {
  font-size: 1.75rem;
  padding-bottom: 0.4em;
  border-bottom: 2px solid #e2e8f0;
}

:deep(h2) {
  font-size: 1.4rem;
  padding-left: 0.7em;
  border-left: 3px solid #3b82f6;
  border-bottom: none;
}

:deep(h3) { font-size: 1.2rem; }
:deep(h4) { font-size: 1.05rem; }
:deep(h5), :deep(h6) { font-size: 0.95rem; color: #475569; }

/* ─── Anchor ─── */
:deep(.header-anchor) {
  opacity: 0;
  position: absolute;
  left: -1em;
  text-decoration: none;
  transition: opacity 0.15s;
}
:deep(h1:hover .header-anchor),
:deep(h2:hover .header-anchor),
:deep(h3:hover .header-anchor),
:deep(h4:hover .header-anchor),
:deep(h5:hover .header-anchor),
:deep(h6:hover .header-anchor) {
  opacity: 0.5;
}

/* ─── Text ─── */
:deep(p) { margin-top: 0; margin-bottom: 1em; }

:deep(ul), :deep(ol) {
  padding-left: 1.8em;
  margin-bottom: 1em;
}

:deep(li + li) { margin-top: 0.2em; }

:deep(li > p) { margin-bottom: 0.4em; }

:deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 1em 0;
}

:deep(hr) {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 2em 0;
}

/* ─── Code Block ─── */
:deep(.code-block-wrapper) {
  position: relative;
  margin: 1.2rem 0;
  border-radius: 10px;
  overflow: hidden;
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
}

:deep(.code-block-header) {
  display: flex;
  align-items: center;
  padding: 0.35em 0.8em;
  background-color: #334155;
  border-bottom: none;
}

:deep(.mac-dots) {
  display: flex;
  gap: 6px;
  margin-right: 0.8em;
}

:deep(.dot) {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

:deep(.dot.red) { background-color: #ef4444; }
:deep(.dot.yellow) { background-color: #f59e0b; }
:deep(.dot.green) { background-color: #22c55e; }

:deep(.language-name) {
  flex-grow: 1;
  text-align: left;
  font-size: 12px;
  font-family: 'SF Mono', 'Fira Code', monospace;
  color: #94a3b8;
  text-transform: lowercase;
  letter-spacing: 0.02em;
}

:deep(.copy-code-btn) {
  padding: 2px 8px;
  font-size: 11px;
  background: transparent;
  border: 1px solid #64748b;
  border-radius: 4px;
  cursor: pointer;
  color: #cbd5e1;
  transition: all 0.15s;
}
:deep(.copy-code-btn:hover) {
  background-color: #475569;
  color: #f1f5f9;
}

:deep(pre) {
  background-color: transparent;
  padding: 1em 1.2em;
  margin: 0;
  border-radius: 0;
  overflow-x: auto;
  border: none;
  white-space: pre;
  word-wrap: normal;
  font-size: 0.9rem;
}

/* ─── Inline Code ─── */
:deep(:not(pre) > code) {
  background-color: #f1f5f9;
  color: #e11d48;
  padding: .15em .35em;
  margin: 0 1px;
  font-size: 88%;
  border-radius: 4px;
  font-family: 'SF Mono', 'Fira Code', Consolas, monospace;
}

/* ─── Blockquote ─── */
:deep(blockquote) {
  padding: 0.8em 1.2em;
  color: #475569;
  border-left: 3px solid #3b82f6;
  margin: 1em 0;
  background-color: #f8fafc;
  border-radius: 0 6px 6px 0;
  font-style: normal;
}

:deep(blockquote p:last-child) { margin-bottom: 0; }

/* ─── Link ─── */
:deep(a) {
  color: #2563eb;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.15s;
}
:deep(a:hover) {
  border-bottom-color: #2563eb;
}

/* ─── Table ─── */
:deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  display: block;
  overflow-x: auto;
  border-spacing: 0;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  font-size: 0.92rem;
}

:deep(th), :deep(td) {
  padding: 0.6rem 0.8rem;
  border: 1px solid #e2e8f0;
  text-align: left;
}

:deep(th) {
  font-weight: 600;
  background-color: #f1f5f9;
  color: #334155;
}

:deep(tr:nth-child(2n)) {
  background-color: #f8fafc;
}

/* ─── KaTeX ─── */
:deep(.katex) {
  font: normal 1.15em KaTeX_Main, Times New Roman, serif;
  line-height: 1.2;
}

:deep(.katex-display) {
  margin: 1em 0;
  overflow-x: auto;
  overflow-y: hidden;
}

:deep(.katex-display > .katex) {
  display: inline-block;
  white-space: nowrap;
}

:deep(.katex .boldsymbol) { font-weight: bold; }
:deep(.katex .amsrm) { font-family: KaTeX_AMS; }
:deep(.katex .mathscr) { font-family: KaTeX_Script; }
:deep(.katex .mathfrak) { font-family: KaTeX_Fraktur; }
:deep(.katex .mathbb) { font-family: KaTeX_AMS; }
:deep(.katex .mathcal) { font-family: KaTeX_Caligraphic; }
:deep(.katex .mathdefault) { font-family: KaTeX_Math; }
:deep(.katex .mathnormal) { font-family: KaTeX_Math; font-style: italic; }
:deep(.katex .mathrm) { font-family: KaTeX_Main; font-style: normal; }
:deep(.katex .mathit) { font-family: KaTeX_Main; font-style: italic; }
:deep(.katex .mathbf) { font-family: KaTeX_Main; font-weight: bold; }
:deep(.katex .mathsf) { font-family: KaTeX_SansSerif; }
:deep(.katex .mathtt) { font-family: KaTeX_Typewriter; }
:deep(.katex-inline) { margin: 0 0.1em; }

:deep(.katex-error) {
  color: #dc2626;
  background-color: #fef2f2;
  padding: 2px 4px;
  border-radius: 3px;
  border: 1px solid #fecaca;
}

/* ─── Responsive ─── */
@media (max-width: 768px) {
  .markdown-body { padding: 1.5em; }
}

@media (max-width: 480px) {
  .markdown-body { padding: 1em; }
  :deep(h1) { font-size: 1.5em; }
  :deep(h2) { font-size: 1.25em; }
  :deep(h3) { font-size: 1.1em; }
}
</style>
