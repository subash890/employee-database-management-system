from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__, template_folder='templates', static_folder='static')

# ---------------- DATABASE CONNECTION ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Subash@007",
    database="employee_db"
)

cursor = conn.cursor()

# ---------------- HOME PAGE ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- ADD EMPLOYEE ----------------
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        full_name = request.form['full_name']
        age = request.form['age']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        salary = request.form['salary']
        joining_date = request.form['joining_date']

        query = """
        INSERT INTO employee (employee_id, full_name, age, email, phone, department, salary, joining_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (employee_id, full_name, age, email, phone, department, salary, joining_date)

        cursor.execute(query, values)
        conn.commit()

        return redirect('/view')

    return render_template('add_employee.html')

# ---------------- VIEW EMPLOYEES ----------------
@app.route('/view')
def view_employees():
    cursor.execute("SELECT * FROM employee")
    employees = cursor.fetchall()
    return render_template('view_employees.html', employees=employees)

# ---------------- DELETE EMPLOYEE ----------------
@app.route('/delete/<int:employee_id>')
def delete_employee(employee_id):
    query = "DELETE FROM employee WHERE employee_id = %s"
    cursor.execute(query, (employee_id,))
    conn.commit()
    return redirect('/view')

# ---------------- UPDATE EMPLOYEE ----------------
@app.route('/update/<int:employee_id>', methods=['GET', 'POST'])
def update_employee(employee_id):
    if request.method == 'POST':
        full_name = request.form['full_name']
        age = request.form['age']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        salary = request.form['salary']
        joining_date = request.form['joining_date']

        query = """
        UPDATE employee
        SET full_name=%s, age=%s, email=%s, phone=%s, department=%s, salary=%s, joining_date=%s
        WHERE employee_id=%s
        """
        values = (full_name, age, email, phone, department, salary, joining_date, employee_id)

        cursor.execute(query, values)
        conn.commit()
        return redirect('/view')

    query = "SELECT * FROM employee WHERE employee_id = %s"
    cursor.execute(query, (employee_id,))
    employee = cursor.fetchone()

    return render_template('update_employee.html', employee=employee)

# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/view')
def view_employees():
    search = request.args.get('search')

    if search:
        query = """
        SELECT * FROM employee
        WHERE full_name LIKE %s OR department LIKE %s
        """
        value = f"%{search}%"
        cursor.execute(query, (value, value))
    else:
        cursor.execute("SELECT * FROM employee")

    employees = cursor.fetchall()
    return render_template('view_employees.html', employees=employees)