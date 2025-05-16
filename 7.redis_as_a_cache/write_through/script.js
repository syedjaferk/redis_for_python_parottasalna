import fs from "fs";
import { createClient } from "redis";


const redisConnectionUrl = "redis://127.0.0.1:6379";
const pythonFilePath = "./content.py";

const writeThroughCodeRecipe = async () => {
    const requirements = ["rgsync", "pymongo==3.12.0"];
    const writeThroughCode = fs.readFileSync(pythonFilePath).toString();
    const client = createClient({ url: redisConnectionUrl });
    await client.connect();
    const params = ["RG.PYEXECUTE", writeThroughCode,
    "REQUIREMENTS", ...requirements];
    try {
        await client.sendCommand(params);
        console.log("RedisGears writeThroughCode set up completed.");
    }
    catch (err) {
        console.error("RedisGears writeThroughCode setup failed !");
        console.error(JSON.stringify(err, Object.getOwnPropertyNames(err), 4));
    }
    process.exit();
};
writeThroughCodeRecipe();