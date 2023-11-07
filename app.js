import express from "express";
import nunjucks from "nunjucks";
import bcrypt from "bcrypt";
import initialize from "./server/passport-config.js";
import passport from "passport"
import flash from "express-flash";
import session from "express-session";
import * as dotenv from "dotenv";
import methodOverride from "method-override";
import multer from "multer";
// import * as db from './server/db.js';
import mongoose from "mongoose";
import * as fs from 'fs';

if (process.env.NODE_ENV !== "production") {
    dotenv.config();
}

const PORT = process.env.SERVER_PORT;
const FLASK_HOST = process.env.FLASK_HOST;
const FLASK_PORT = process.env.FLASK_PORT;
const uri = process.env.DATABASE_URL;

const app = express();

// multer middleware for file upload
const upload = multer({ dest: "server/uploads/" });

mongoose.connect(uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

const UserSchema = new mongoose.Schema({
    email: {
        type: String,
        required: true
    },
    password: {
        type: String,
        required: true
    }
});

const User = mongoose.model('User', UserSchema);

initialize(passport, User);

app.use("/static", express.static("client/static"));
app.use("/uploads", express.static("server/uploads"));
app.use("/output", express.static("server/output"));

app.use(express.urlencoded({ extended: false }));
app.use(flash());
app.use(session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false
}));
app.use(passport.initialize());
app.use(passport.session());
app.use(methodOverride("_method"));
app.use(express.json());

nunjucks.configure('client/templates', {
    autoescape: true,
    express: app
});

app.get("/", (req, res) => {
    res.render("home.html");
});

app.get("/about", (req, res) => {
    res.render("about.html");
});

app.get("/single", checkAuthenticated, (req, res) => {
    res.render("single.html");
});

app.get("/batch", (req, res) => {
    res.render("batch.html");
});

app.get("/batch", checkAuthenticated, (req, res) => {
    res.render("batch.html");
});

app.get("/history", checkAuthenticated, (req, res) => {
    res.render("history.html");
});

app.get("/signup", checkNotAuthenticated, (req, res) => {
    res.render("signup.html");
});

// POST login info to the database
app.post("/signup", async (req, res) => {
    try {
        const exists = await User.exists({ email: req.body.email });

        if (exists) {
            res.redirect('/login');
            return;
        }

        const hashedPass = await bcrypt.hash(req.body.password, 10);
        new User({
            email: req.body.email,
            password: hashedPass
        }).save();
        res.redirect("/login");
    } catch {
        res.redirect("/signup");
    }
});

app.get("/login", checkNotAuthenticated, (req, res) => {
    res.render("login.html");
});

// POST login info to the Authenticator
app.post("/login", passport.authenticate("local", {
    successRedirect: "/",
    failureRedirect: "/login",
    failureFlash: true
}));

// Logout route
app.get("/logout", checkAuthenticated, (req, res) => {
    req.logout(function (err) {
        if (err) { return next(err); }
        res.redirect('/login');
    });
});

// Checks if user is authenticated
function checkAuthenticated(req, res, next) {
    if (req.isAuthenticated()) {
        return next();
    }
    res.redirect("/login");
    // return next(); // Used to skip m andatory login
}

// Checks if user is not authenticated
function checkNotAuthenticated(req, res, next) {
    if (req.isAuthenticated()) {
        return res.redirect("/");
    }
    next();
}

app.post("/single-clean", upload.fields([{ name: 'image' }, { name: 'mask' }]), async (req, res) => {
    const files = req.files;

    const image_file = files["image"][0];
    const mask_file = files["mask"][0];

    let img = Buffer.from(fs.readFileSync(image_file["path"])).toString('base64')
    const mask = Buffer.from(fs.readFileSync(mask_file["path"])).toString('base64')

    const response = await fetch(`http://${FLASK_HOST}:${FLASK_PORT}/single-clean`, {
        timeout: 10000,
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "img": { "img": img, "name": image_file.originalname }, "mask": { "img": mask, "name": mask_file.originalname } })
    });

    const responseData = await response.json();

    if (responseData["success"]) {
        let new_img = Buffer.from(responseData["img"], 'base64')
        await fs.writeFile(`./server/uploads/${responseData["name"]}`, new_img, err => { });

        db.save_img(responseData["name"], `/uploads/${responseData["name"]}`);

        res.render("single_clean.html", { file: `./uploads/${responseData["name"]}` })
    } else {
        res.redirect("/single");
    }
});

app.post("/batch-clean", upload.array('images', 10), async (req, res) => {
    const files = req.files;

    let imgs = [];

    for (let file of files) {
        imgs.push({
            "img": Buffer.from(fs.readFileSync(file["path"])).toString('base64'),
            "name": file.originalname
        })
    }

    const response = await fetch(`http://${FLASK_HOST}:${FLASK_PORT}/batch-clean`, {
        timeout: 10000,
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(imgs)
    });

    const responseData = await response.json();

    if (responseData["success"]) {
        let clean_imgs = responseData["imgs"];
        for (let img of clean_imgs) {
            let new_img = Buffer.from(img["img"], 'base64');
            await fs.writeFile(`./server/output/${img["name"]}`, new_img, err => { });

            db.save_img(img["name"], `/output/${img["name"]}`);
        }

        res.render("batch_clean.html")
    } else {
        res.redirect("/batch");
    }
});

app.get("/history", async (req, res) => {
    res.render("history.html");
});

// app.post("/search", async (req, res) => {
//     let imgs = await db.get_img(req.body["img"]);
//     res.status(200).json(imgs)
// });

// app.post("/search_all", async (req, res) => {
//     let imgs = await db.get_all_imgs();
//     res.status(200).json(imgs)
// });

app.get("/get_cleaned", async (req, res) => {
    let files = [];

    fs.readdirSync("./server/output").forEach(file => {
        files.push(file);
    });

    files = files.filter(file => file !== ".placeholder");

    res.status(200).json(files);
});

app.listen(PORT, () => {
    console.log(`Express server listening on port ${PORT}`);
});