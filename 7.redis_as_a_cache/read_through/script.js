import fs from "fs";
import { createClient } from "redis";


const redisConnectionUrl = "redis://127.0.0.1:6379";
const pythonFilePath = "./read_script.py";

const runReadThroughRecipe = async () => {
    const requirements = ["pymongo==3.12.0"];
    const readThroughCode = fs.readFileSync(pythonFilePath).toString();
    const client = createClient({ url: redisConnectionUrl });
    await client.connect();
    const params = ["RG.PYEXECUTE", readThroughCode,
    "REQUIREMENTS", ...requirements];
    try {
        await client.sendCommand(params);
        console.log("RedisGears ReadThrough set up completed.");
    }
    catch (err) {
        console.error("RedisGears ReadThrough setup failed !");
        console.error(JSON.stringify(err, Object.getOwnPropertyNames(err), 4));
    }
    process.exit();
};
runReadThroughRecipe();