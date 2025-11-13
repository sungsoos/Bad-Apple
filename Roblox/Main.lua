-- LocalScript (StarterPlayerScripts)

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local frameModules = {}

for _, child in ipairs(ReplicatedStorage:GetChildren()) do
	local n = child.Name:match("^BadAppleFrames_Part(%d+)$")
	if n then
		frameModules[tonumber(n)] = child
	end
end

local player = Players.LocalPlayer
local frames = {}
local W,H,FPS,USE_RLE
for i = 1, #frameModules do
	local chunk = require(frameModules[i])
	if not W then W,H,FPS,USE_RLE = chunk.width,chunk.height,chunk.fps,chunk.rle end
	for _, f in ipairs(chunk.frames) do
		table.insert(frames,f)
	end
end

local PIXEL_SIZE = 1
local GAP = 0.0
local BASE_POS = Vector3.new(0,0.5,0)
local BLACK = Color3.new(0,0,0)
local WHITE = Color3.new(1,1,1)
local PRE_DECODE = true

local decoded = {}
if PRE_DECODE then
	for i=1,#frames do
		if USE_RLE then decoded[i] = (function()
				local s=frames[i]
				local out={}
				for token in string.gmatch(s,"[^,]+") do
					local c=string.sub(token,1,1)
					local n=tonumber(string.sub(token,2))
					local bit = (c=="B") and "1" or "0"
					for _=1,n do table.insert(out,bit) end
				end
				return table.concat(out)
			end)() else decoded[i]=frames[i] end
	end
end

-- container
local root = workspace:FindFirstChild("BadAppleDisplay")
if root then root:Destroy() end
root = Instance.new("Model")
root.Name = "BadAppleDisplay"
root.Parent = workspace

local parts = {}
local offsetX, offsetZ = PIXEL_SIZE + GAP, PIXEL_SIZE + GAP
for row = 1, H do
	for col = 1, W do
		local p = Instance.new("Part")
		p.Size = Vector3.new(PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
		p.Anchored = true
		p.CanCollide = true
		p.Color = WHITE
		p.TopSurface = Enum.SurfaceType.Studs
		p.BottomSurface = Enum.SurfaceType.Studs

		local xPos = BASE_POS.X + (W - col) * offsetX
		local zPos = BASE_POS.Z - (row - 1) * offsetZ
		p.Position = Vector3.new(xPos, BASE_POS.Y, zPos)
		p.Parent = root

		table.insert(parts, p)
	end
end



local function playBadApple()
	local frameTime = 1 / FPS
	local current = 1
	local lastTime = tick()
	local connection
	connection = RunService.RenderStepped:Connect(function()
		local now = tick()
		if now - lastTime >= frameTime then
			lastTime = now
			if current > #frames then
				connection:Disconnect()
				return
			end

			local s = PRE_DECODE and decoded[current] or (USE_RLE and decodeRLE(frames[current]) or frames[current])
			for i = 1, #parts do
				local bit = string.sub(s, i, i)
				parts[i].Color = (bit == "1") and BLACK or WHITE
			end

			current += 1
		end
	end)
end

player.Chatted:Connect(function(msg)
	if msg:lower() == "!start" then
		playBadApple()
	end
end)

warn(("Bad Apple ready. Type !start in chat to play (%d frames, %dx%d, %d FPS)").format(#frames,W,H,FPS))
