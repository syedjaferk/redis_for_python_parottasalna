import fs from "fs";
import { createClient } from "redis";


const redisConnectionUrl = "redis://127.0.0.1:6379";
const pythonFilePath = "app.py";

const runWriteBehindRecipe = async () => {
    const requirements = ["rgsync", "pymongo==3.12.0"];
    const writeBehindCode = fs.readFileSync(pythonFilePath).toString();
    const client = createClient({ url: redisConnectionUrl });
    await client.connect();
    const params = ["RG.PYEXECUTE", writeBehindCode,
    "REQUIREMENTS", ...requirements];
    try {
        await client.sendCommand(params);
        console.log("RedisGears WriteBehind set up completed.");
    }
    catch (err) {
        console.error("RedisGears WriteBehind setup failed !");
        console.error(JSON.stringify(err, Object.getOwnPropertyNames(err), 4));
    }
    process.exit();
};
runWriteBehindRecipe();