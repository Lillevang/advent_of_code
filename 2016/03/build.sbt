val scala3Version = "3.2.1"

lazy val root = project
    .in(file("."))
    .settings(
        name := "2016-03",
        version := "0.1.0-SNAPSHOT",
        scalaVersion := scala3Version,
    )
