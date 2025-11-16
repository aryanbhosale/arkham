// Vitest config that works with npx
export default {
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    css: true,
    env: {
      NODE_ENV: 'test',
    },
  },
}

