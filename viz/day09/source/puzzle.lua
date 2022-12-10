local function readPuzzle()
    local file<const> = playdate.file.open("input.txt", playdate.file.kFileRead)
    assert(file)
    local puzzle<const> = {}
    while true do
        local line = file:readline()
        if not line then break end
        dir, amt = string.match(line, "([RLUD]) (%d+)")
        table.insert(puzzle, {dir, tonumber(amt)})
    end
    return puzzle
end

local function doPuzzle(dirs)
    coroutine.yield()

    local puzzle<const> = readPuzzle()
    coroutine.yield()

    for _, move in ipairs(puzzle) do
        local dirName<const> = move[1]
        local amt<const> = move[2]
        local moveDir<const> = dirs[dirName]

        for _ = 1, amt do
            moveDir()
            coroutine.yield()
        end
    end
end

class("Puzzle").extends()

function Puzzle:init(dirs)
    self.co = coroutine.create(doPuzzle)
    coroutine.resume(self.co, dirs)
end

function Puzzle:run() coroutine.resume(self.co) end

function Puzzle:stop() coroutine.close(self.co) end

function Puzzle:isRunning() return coroutine.status(self.co) ~= "dead" end
