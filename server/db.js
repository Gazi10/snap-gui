import pkg from "pg";
const { Client } = pkg;

const client = new Client({
    host: process.env.POSTGRES_DB,
    user: "postgres",
    // password: process.env.POSTGRES_PASSWORD,
    password: "secure_db_password",
    database: "suiep"
});

await client.connect();

export async function save_img(img_name, img_path) {
    await client.query("INSERT INTO images (image_name,image_path) VALUES ($1::text,$2::text)", [img_name, img_path]);
}

export async function get_img(img_name) {
    let res = await client.query("SELECT * FROM images WHERE image_name = $1::text", [img_name]);
    if (res.rowCount > 0)
        return res.rows;
    return {}
}

export async function get_all_imgs() {
    let res = await client.query("SELECT * FROM images");
    return res.rows;
}
