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
class QueryResultError extends Error {
  constructor(message = "No result.") {
    super(message);
    this.name = "QueryResultError";
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

  try {
    const SUCCESS_MESSAGE = "Successful database query";
    const state = params.state;
    if (state === "" || state === null || state == undefined) {
      throw new TypeError(
        "Requried parameter is missing.",
        "dealership_by_state.js",
        39
      );
    }
    const cloudant = Cloudant({
      url: URL,
      plugins: { iamauth: { iamApiKey: API_KEY } },
    });
    const query = {
      selector: {
        st: { $eq: state },
      },
      limit: 50,
    };
    let db = await cloudant.use(db_name);
    let dealershipsByState = await db.find(query);
    if (dealershipsByState.docs.length === 0) {
      throw new QueryResultError("The state does not exist.");
    }
    logger.info(" The query was succesful.");
    //logger.debug(dealershipsByState);
    httpResponse.body = {
      message: SUCCESS_MESSAGE,
      docs: dealershipsByState,
    };
    return httpResponse;
  } catch (err) {
    logger.error(err.message);
    err.statusCode ? logger.error(err.statusCode) : 0;
    errorMessage = err.message ? err.message : err.description;
    httpResponse.body = {
      error: errorMessage,
      message: "Something went wrong on the server",
    };
    httpResponse.statusCode = err.statusCode ? err.statusCode : "500";
    return httpResponse;
  }
}
