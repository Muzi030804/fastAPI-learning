/**
 * API 配置文件
 * 包含后端接口地址，以及千问AI平台（OpenAI 兼容模式）的调用参数
 */

// 后端 API 基础地址
export const apiConfig = {
  baseURL: 'http://127.0.0.1:8000',
}

// 千问AI平台 OpenAI 兼容模式的基础地址
// 注意：控制台上显示的是 maas.qianwenai.com，实际可用域名是 maas.qianwenaiapi.com
const QWEN_BASE_URL = 'https://maas.qianwenaiapi.com/compatible-mode/v1'

export const aiChatConfig = {
  // ===== 只需修改这一行：填入你在千问AI平台创建的 API Key =====
  apiKey: '',

  // 模型 ID（Qwen3.6-Flash 在平台上的模型名是 qwen3.6-flash）
  model: 'qwen3.6-flash',

  // 请求地址 = 基础地址 + /chat/completions，无需修改
  apiEndpoint: `${QWEN_BASE_URL}/chat/completions`,
}