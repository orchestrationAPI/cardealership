const Cloudant = require("@cloudant/cloudant");
const log4js = require("log4js");
const logger = log4js.getLogger();
logger.level = "debug";

class EmptyDatabaseError extends Error {
  constructor(message = "The database is empty.") {
    super(message);
    this.name = "EmptyDatabase";
    this.statusCode = 404;
    // init
  }
}

async function main(params) {
  const URL = params.__bx_creds.cloudantnosqldb.url;
  const API_KEY = params.__bx_creds.cloudantnosqldb.apikey;
  const db_name = "dealerships";
  const httpResponse = {
    body: {},
    statusCode: 200,
    headers: { "Content-Type": "application/json" },
  };
  const cloudant = Cloudant({
    url: URL,
    plugins: { iamauth: { iamApiKey: API_KEY } },
  });

  try {
    const SUCCESS_MESSAGE = 'Successful database query'
    let db = await cloudant.use(db_name);
    let dealerships = await db.list({ include_docs: true });
    if (dealerships.rows.length === 0) {
      throw new EmptyDatabaseError();
    }
    logger.info(" The query was succesful.");
    httpResponse.body = { 
	    message : SUCCESS_MESSAGE,
	    docs: dealerships.rows };
    return httpResponse;
  } catch (err) {
    logger.error(err.message);
    err.statusCode ? logger.error(err.statusCode) : null;
    errorMessage = err.message ? err.message : err.description;
    httpResponse.body = {
      error: errorMessage,
      message: "Something went wrong on the server",
    };
    httpResponse.statusCode = err.statusCode ? err.statusCode : "500";
    return httpResponse;
  }
}
