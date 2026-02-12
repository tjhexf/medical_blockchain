CREATE DATABASE hospital;
USE hospital;

CREATE TABLE paciente (
	id_paciente		INT AUTO_INCREMENT PRIMARY KEY,
	nome			VARCHAR(255),
	cpf				VARCHAR(11),
	telefone		VARCHAR(20),
)

CREATE TABLE medico (
	id_medico		INT AUTO_INCREMENT PRIMARY KEY,
	nome			VARCHAR(255),
	cpf				VARCHAR(11),
	crm				VARCHAR(20),
	especialidade	VARCHAR(255),
	telefone		VARCHAR(20),
)

CREATE TABLE consultas (
	id INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT,
    id_medico INT,
    data_consulta DATETIME,
    diagnostico TEXT,
    tratamento TEXT,
    receita TEXT,
    FOREIGN KEY (id_paciente) REFERENCES paciente(id),
    FOREIGN KEY (id_medico) REFERENCES medico(id) 
)

INSERT INTO paciente (nome, cpf, telefone)
VALUES
('José Silveira', '11122233344', '956789555'),
('Camila Souza', '22233344455', '956789599'),
('Gerson Cavalheiro', '56756756711', '932779598');

INSERT INTO medico (nome, cpf, crm, especialidade, telefone)
VALUES
('João Silva', '12345678900', '654321', 'Cardiologia', '987654321'),
('Maria dos Santos', '99999999999', '123456', 'Pediatria', '980028922'),
('Anderson Ferrugem', '11111111111', '222222', 'Otorrinolaringologista', '970707070');
