# Final Project

## Team Members
- Sharon Zou *(Period 4)*
- Christina Tan *(Period 4)*

## Features Implemented:

- Mesh ▦ 🥴:
    - `mesh: fileName` : Reads in an external .obj file (ex: "cloud") for polygons and displays it

- Primitive Shapes 🔺🔵:
    - `cone cx cy cz r h` : creates a cone centered at cx cy cz with height h
    - `pyramid cx cy cz b h` : creates a pyramid centered at cx cy cz with base b and height h
    - `cylinder cx cy cz r h` : creates a cylinder centered at cx cy cz with radius r and height h

- Changed behavior of vary. Added a parameter to change how it calculates the change over time.
  Default is linear. To invoke exponential or logarithmic behavior, use syntax below 👇:
  *This feature was attempted but not completely successful*
    - Exponential : `vary spinny 0 49 0 1 exponential`
    - Logarithmic : `vary spinny 0 49 0 1 logarithmic`
