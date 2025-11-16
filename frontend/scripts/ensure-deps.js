#!/usr/bin/env node
/**
 * Ensure required dependencies are installed
 */
import { execSync } from 'child_process'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const nodeModulesPath = path.join(__dirname, '..', 'node_modules')

const requiredPackages = [
  { name: 'vite', version: '5.0.8' },
  { name: '@vitejs/plugin-react', version: '4.2.1' },
  { name: 'tailwindcss', version: '3.3.6' },
  { name: 'autoprefixer', version: '10.4.16' },
  { name: 'postcss', version: '8.4.32' },
  { name: '@tailwindcss/typography', version: '0.5.10' },
]

function checkAndInstall(packageName, version) {
  const packagePath = packageName.startsWith('@') 
    ? path.join(nodeModulesPath, ...packageName.split('/'))
    : path.join(nodeModulesPath, packageName)
  
  if (!fs.existsSync(packagePath)) {
    console.log(`Installing ${packageName}@${version}...`)
    try {
      execSync(`npm install ${packageName}@${version} --save-dev --legacy-peer-deps`, {
        stdio: 'inherit',
        cwd: path.join(__dirname, '..')
      })
    } catch (error) {
      console.error(`Failed to install ${packageName}:`, error.message)
      return false
    }
  }
  return true
}

// Install all required packages
console.log('Ensuring required dependencies are installed...')
let allInstalled = true
for (const pkg of requiredPackages) {
  if (!checkAndInstall(pkg.name, pkg.version)) {
    allInstalled = false
  }
}

if (allInstalled) {
  console.log('✓ All dependencies installed')
} else {
  console.log('⚠ Some dependencies failed to install')
  process.exit(1)
}

