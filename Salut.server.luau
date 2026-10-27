-- Staff12 | script de test pentru GitHub Loader
-- Acest cod este executat de Loader pe SERVER la pornirea jocului.
-- Nu sterge sau modifica anticheatul existent.

local folder = Instance.new("Folder")
folder.Name = "Staff12_GitHubLoaded"
folder:SetAttribute("Source", "GitHub/Salut.server.luau")
folder.Parent = game:GetService("ServerStorage")

print("Salut, s-a activat!")
return true
