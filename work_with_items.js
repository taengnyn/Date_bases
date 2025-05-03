db.items.find().pretty()

db.items.countDocuments({ category: "Phone" })

db.items.distinct("category").length

db.items.distinct("producer")

db.items.find({
  $and: [
    { category: "Phone" },
    { price: { $gte: 500, $lte: 800 } }
  ]
})


db.items.find({
  $or: [
    { model: "iPhone 6" },
    { model: "Samsung Galaxy S21" }
  ]
})


db.items.find({
  producer: { $in: ["Apple", "Samsung"] }
})


db.items.updateMany(
  { category: "Tablet" },
  { $set: { price: 999 } }
)


db.items.updateMany(
  { category: "Phone" },
  { $set: { colour: "dark" } }
)

db.items.find({})



db.items.find({
  colour: { $exists: true }
})


db.items.updateMany(
  { colour: { $exists: true } },
  { $inc: { price: 190 } }
)

db.items.find({})



db.orders.insertMany([
  {
    customer: { name: "Ivan Petrov", credit_card: "1234-5678-9012-3456" },
    date: ISODate("2025-04-01T10:00:00Z"),
    items: [
      ObjectId("6816048acf436847a7a41bc1"),
      ObjectId("6816048acf436847a7a41bc3"),
    ],
    total_price: 1040
  },
  {
    customer: { name: "Anna Kovalenko", credit_card: "9876-5432-1098-7654" },
    date: ISODate("2025-04-15T15:30:00Z"),
    items: [
      ObjectId("6816048acf436847a7a41bc4"),
      ObjectId("6816048acf436847a7a41bc3"),
      ObjectId("6816048acf436847a7a41bc6"),
    ],
    total_price: 1638
  },
  {
    customer: { name: "Ivan Petrov", credit_card: "1234-5678-9012-3456" },
    date: ISODate("2025-05-01T08:45:00Z"),
    items: [
      ObjectId("6816048acf436847a7a41bca"),
      ObjectId("6816048acf436847a7a41bce")
    ],
    total_price: 1808
  }
])

db.orders.find().pretty()

db.orders.find({ total_price: { $gt: 1300 } })


db.orders.find({ "customer.name": "Ivan Petrov" })


db.orders.find({ items: ObjectId("680f90decf436847a7a41af9") })


db.orders.updateMany(
  { items: ObjectId("644b1a8e3e9f1dba5a132c3a") },
  {
    $push: { items: ObjectId("644b1a8e3e9f1dba5a132c3e") },
    $inc: { total_price: 200 }
  }
)


db.orders.aggregate([
  { $match: { _id: ObjectId("680fa3886e5feba5d444152f") } },
  { $project: { numberOfItems: { $size: "$items" } } }
])



db.orders.find(
  { total_price: { $gt: 1600 } },
  { "customer.name": 1, "customer.credit_card": 1 }
)
db.orders.find({ date: { $exists: true } }, { date: 1 })


db.orders.find({
  date: {
    $gte: ISODate("2025-04-01T00:00:00Z"),
    $lte: ISODate("2025-04-16T23:59:59Z")
  },
  items: ObjectId("6816048acf436847a7a41bc3")
}).pretty()



db.orders.updateMany(
  {
    date: { $gte: ISODate("2025-04-01"), $lte: ISODate("2025-04-16") }
  },
  {
    $pull: { items: ObjectId("6816048acf436847a7a41bc3") }
  }
)


db.orders.find({
  date: {
    $gte: ISODate("2025-04-01T00:00:00Z"),
    $lte: ISODate("2025-04-16T23:59:59Z")
  },
  items: ObjectId("6816048acf436847a7a41bc3")
}).pretty()


db.orders.updateMany(
  { "customer.name": "Олена Іваненко" },
  { $set: { "customer.name": "Катерина Мироненко" } }
)

db.orders.find({})

db.orders.aggregate([
  { $match: { "customer.name": "Катерина Мироненко" } },
  {
    $lookup: {
      from: "items",
      localField: "items",
      foreignField: "_id",
      as: "detailed_items"
    }
  },
  {
    $project: {
      _id: 0,
      customer: 1,
      detailed_items: { model: 1, price: 1 }
    }
  }
])

db.createCollection("reviews", {
  capped: true,
  size: 4096,   // розмір у байтах (мінімум кілька КБ)
  max: 5        // максимум 5 документів
})

db.reviews.insertMany([
  { user: "Олег", rating: 5, comment: "Все супер!", date: new Date("2025-05-01T10:00:00Z") },
  { user: "Ірина", rating: 4, comment: "Добре, але довга доставка", date: new Date("2025-05-01T12:00:00Z") },
  { user: "Андрій", rating: 3, comment: "Очікував кращого", date: new Date("2025-05-01T14:00:00Z") },
  { user: "Марія", rating: 5, comment: "Швидко і якісно", date: new Date("2025-05-01T16:00:00Z") },
  { user: "Тарас", rating: 2, comment: "Прийшло не те", date: new Date("2025-05-01T18:00:00Z") },
])

db.reviews.find().sort({ date: 1 }).pretty()

db.reviews.insertOne({
  user: "Юлія",
  rating: 5,
  comment: "Дуже задоволена сервісом!",
  date: new Date("2025-05-01T22:00:00Z")
})

db.reviews.find().sort({ date: 1 }).pretty()