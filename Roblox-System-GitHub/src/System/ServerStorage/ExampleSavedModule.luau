-- ModuleScript din ServerStorage. Nu rulează singur.
local Module = {}
function Module.Greet(name)
    return "Salut, " .. tostring(name) .. "!"
end
return Module
