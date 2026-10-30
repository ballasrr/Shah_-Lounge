// Запуск всего проекта одной командой: npm start — бэкенд на :8000 и сайт на :3000.
// Ctrl+C останавливает оба; если один упал, второй тоже останавливается.
import { spawn, spawnSync } from 'node:child_process'
import { existsSync } from 'node:fs'
import { fileURLToPath } from 'node:url'

const root = fileURLToPath(new URL('..', import.meta.url))
const backend = fileURLToPath(new URL('../backend', import.meta.url))
const win = process.platform === 'win32'
const python = win ? '.venv\\Scripts\\python' : '.venv/bin/python'

if (!existsSync(new URL(`../backend/${python.replaceAll('\\', '/')}${win ? '.exe' : ''}`, import.meta.url))) {
  console.error('Нет backend/.venv: создайте его по инструкции из backend/README.md')
  process.exit(1)
}

const procs = [
  spawn(`${python} -m uvicorn app.main:app --host 127.0.0.1 --port 8000`, { cwd: backend, shell: true, stdio: 'inherit' }),
  spawn('npm run dev -- --host 127.0.0.1', { cwd: root, shell: true, stdio: 'inherit' })
]

let stopping = false
function stop(code = 0) {
  if (stopping) return
  stopping = true
  for (const p of procs) {
    if (p.exitCode !== null) continue
    // на Windows обычный kill не трогает дочерние процессы оболочки
    if (win) spawnSync('taskkill', ['/PID', String(p.pid), '/T', '/F'], { stdio: 'ignore' })
    else p.kill()
  }
  process.exit(code)
}

for (const p of procs) p.on('exit', code => stop(code ?? 0))
process.on('SIGINT', () => stop())
process.on('SIGTERM', () => stop())
