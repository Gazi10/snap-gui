import LocalStrategy from "passport-local";
import bcrypt from "bcrypt";

function initialize(passport, User) {
  const authenticateUser = async (email, password, done) => {
    const user =  await User.findOne({ email: email })
    
    if (user === null) {
      return done(null, false, { message: "User with that email doesn't exist" });
    }

    try {
      if (await bcrypt.compare(password, user.password)) {
        return done(null, user);
      } else {
        return done(null, false, { message: "Password incorrect" });
      }
    } catch (e) {
      return done(e);
    }
  }

  const findId = async (id) => await User.findById(id);

  passport.use(new LocalStrategy({ usernameField: "email"}, authenticateUser));
  passport.serializeUser((user, done) => done(null, user.id));
  passport.deserializeUser((id, done) => done(null, findId(id)));
}

export default initialize;
