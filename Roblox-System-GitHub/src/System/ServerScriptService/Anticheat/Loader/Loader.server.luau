-- Script: ServerScriptService/Anticheat/Loader/Loader
local Players = game:GetService("Players")
local Anticheat = script.Parent.Parent
local Settings = require(Anticheat.Config.Settings)
local Version = require(Anticheat.Version)

local Loader = {}
local started = false
local function checkPlayer(player)
    local function onCharacter(character)
        local humanoid = character:WaitForChild("Humanoid", 10)
        if not humanoid then return end
        task.spawn(function()
            while player.Parent == Players and humanoid.Parent and humanoid.Health > 0 do
                task.wait(Settings.CheckInterval)
                if not Settings.Enabled then continue end
                if humanoid.WalkSpeed > Settings.MaxWalkSpeed then
                    warn(("[Anticheat %s] %s: WalkSpeed %.1f > %.1f"):format(
                        Version.Number, player.Name, humanoid.WalkSpeed, Settings.MaxWalkSpeed))
                    if Settings.KickOnInvalidWalkSpeed then
                        player:Kick("Suspicious movement detected")
                        break
                    end
                end
            end
        end)
    end
    player.CharacterAdded:Connect(onCharacter)
    if player.Character then task.spawn(onCharacter, player.Character) end
end

function Loader.Start()
    if started then return end
    started = true
    if Settings.Debug then print("[Loader] " .. Version.Name .. " v" .. Version.Number .. " pornit") end
    Players.PlayerAdded:Connect(checkPlayer)
    for _, player in Players:GetPlayers() do task.spawn(checkPlayer, player) end
end

Loader.Start()
