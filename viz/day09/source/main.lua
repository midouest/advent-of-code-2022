import "CoreLibs/object"
import "CoreLibs/graphics"
import "CoreLibs/sprites"
import "CoreLibs/timer"
import "CoreLibs/crank"

local pd<const> = playdate
local gfx<const> = pd.graphics

local screenWPx<const>, screenHPx<const> = pd.display.getSize()
local tilePx<const> = 20
local screenWTile<const> = screenWPx / tilePx
local screenHTile<const> = screenHPx / tilePx

local minRopeLength<const> = 2
local maxRopeLength<const> = 10
local startX<const> = 0
local startY<const> = 0

local visited
local rope
local ropeCoords
local ropeLength
local isDirty
local viewX
local viewY

local function coordKey2(x, y)
    return tostring(math.tointeger(x)) .. "," .. tostring(math.tointeger(y))
end
local function coordKey1(coord) return coordKey2(coord[1], coord[2]) end

local function sgn(n)
    if n > 0 then
        return 1
    elseif n < 0 then
        return -1
    end
    return 0
end

local function markVisited() visited[coordKey1(rope[ropeLength])] = true end

local function updateRopeCoords()
    ropeCoords = {}
    for i = 1, ropeLength do
        local key<const> = coordKey1(rope[i])
        local indices<const> = ropeCoords[key]
        if indices == nil then ropeCoords[key] = i end
    end
end

local function moveRope(axis, step)
    local prev = rope[1]
    prev[axis] = prev[axis] + step
    for i = 2, ropeLength do
        local curr<const> = rope[i]
        local dx<const> = prev[1] - curr[1]
        local dy<const> = prev[2] - curr[2]
        if math.abs(dx) > 1 or math.abs(dy) > 1 then
            curr[1] = curr[1] + sgn(dx)
            curr[2] = curr[2] + sgn(dy)
        end
        prev = curr
    end
    updateRopeCoords()
    markVisited()
    isDirty = true
end

local function shortenRope()
    if ropeLength == minRopeLength then return end
    table.remove(rope, ropeLength)
    ropeLength = ropeLength - 1
    markVisited()
    updateRopeCoords()
    isDirty = true
end

local function lengthenRope()
    if ropeLength == maxRopeLength then return end
    local tail<const> = rope[ropeLength]
    table.insert(rope, {tail[1], tail[2]})
    ropeLength = ropeLength + 1
    updateRopeCoords()
    isDirty = true
end

function setUpGame()
    visited = {}
    rope = {}
    ropeCoords = {}
    ropeLength = minRopeLength
    isDirty = true
    viewX = startX - (screenWTile // 2) + 1
    viewY = startY - (screenHTile // 2) + 1

    for _ = 1, ropeLength do table.insert(rope, {startX, startY}) end
    updateRopeCoords()
    markVisited()
end

function setUpMenu()
    local menu<const> = pd.getSystemMenu()
    menu:addMenuItem("Reset", setUpGame)
end

setUpMenu()
setUpGame()

local function moveLeft()
    moveRope(1, -1)
    if rope[1][1] < viewX + 1 then viewX = viewX - 1 end
end
local function moveRight()
    moveRope(1, 1)
    if rope[1][1] > viewX + screenWTile - 2 then viewX = viewX + 1 end
end
local function moveUp()
    moveRope(2, -1)
    if rope[1][2] < viewY + 1 then viewY = viewY - 1 end
end
local function moveDown()
    moveRope(2, 1)
    if rope[1][2] > viewY + screenHTile - 2 then viewY = viewY + 1 end
end

function pd.leftButtonDown() moveLeft() end
function pd.rightButtonDown() moveRight() end
function pd.upButtonDown() moveUp() end
function pd.downButtonDown() moveDown() end

function pd.BButtonDown() shortenRope() end
function pd.AButtonDown() lengthenRope() end

local function tileToScreen(x, y)
    return (x - viewX) * tilePx, (y - viewY) * tilePx
end

local function drawTile(text, x, y)
    local sx<const>, sy<const> = tileToScreen(x, y)
    gfx.drawTextInRect(text, sx, sy, tilePx, tilePx, nil, nil,
                       kTextAlignment.center)
end

local function ropeTile(i)
    if i == 1 then
        return "H"
    elseif i == ropeLength and ropeLength == 2 then
        return "T"
    end
    return tostring(i - 1)
end

local function redraw()
    gfx.clear(gfx.kColorBlack)
    gfx.setImageDrawMode(gfx.kDrawModeFillWhite)

    for yOff = 0, screenHTile - 1 do
        local y<const> = viewY + yOff
        for xOff = 0, screenWTile - 1 do
            local x<const> = viewX + xOff
            local key<const> = coordKey2(x, y)
            local tile = "."
            local i = ropeCoords[key]
            if i ~= nil then
                tile = ropeTile(i)
            elseif x == startX and y == startY then
                tile = "s"
            elseif visited[key] ~= nil then
                tile = "#"
            end
            drawTile(tile, x, y)
        end
    end
end

function pd.update()
    if isDirty then
        redraw()
        isDirty = false
    end

    pd.timer.updateTimers()
    pd.drawFPS(0, 0)
end
