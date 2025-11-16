// Vite config - plugins loaded dynamically
export default async () => {
  // Dynamically import plugins when available via npx
  let reactPlugin = null
  try {
    const react = await import('@vitejs/plugin-react')
    reactPlugin = react.default()
  } catch (e) {
    // Plugin not available yet, will be loaded by npx
  }

  return {
    plugins: reactPlugin ? [reactPlugin] : [],
    server: {
      port: 3000,
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
        },
      },
    },
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: './src/test/setup.ts',
      css: true,
    },
  }
}

