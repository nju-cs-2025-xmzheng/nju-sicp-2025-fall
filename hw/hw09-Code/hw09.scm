;;; Homework 09: Macro

; ANSWER QUESTION wwsd

;;; Required Problems

(define (find n lst)
  (define (helper lst result)
    (if (= (car lst) n)
      result
      (helper (cdr lst) (+ result 1))
    )
  )
  (helper lst 0)
)


(define (find-nest n sym)
  (define (helper sym result)
    (cond
      ((eq? n sym) result)
      ((pair? sym)
        (if (helper (car sym) `(car ,result))
          (helper (car sym) `(car ,result))
          (helper (cdr sym) `(cdr ,result))
        )
      )
      (else #f)
    )
  )
  (helper (eval sym) sym)
)


(define-macro (my/or operands)
  (cond 
    ((null? operands) #f)
    ((null? (cdr operands)) (car operands))
    (else
      `(let ((t ,(car operands)))
        (if t
          t
          (my/or ,(cdr operands))
        )
      )
    )
  )
)


(define-macro (k-curry fn args vals indices)
  (define (h1 args indices i)
    (cond
      ((null? args) '())
      ((and (not (null? indices)) (= i (car indices)))
        (h1 (cdr args) (cdr indices) (+ i 1)))
      (else (cons (car args)
        (h1 (cdr args) indices (+ i 1))))
    )
  )
  (define (h2 args vals indices i)
    (cond
      ((null? args) '())
      ((and (not (null? indices)) (= i (car indices)))
        (cons (car vals) (h2 (cdr args) (cdr vals) (cdr indices) (+ i 1))))
      (else (cons (car args)
        (h2 (cdr args) vals indices (+ i 1))))
    )
  )
  `(lambda ,(h1 args indices 0) ,(cons fn (h2 args vals indices 0)))
)


(define-macro (let* bindings expr)
  (if (null? bindings)
    `(let () ,expr)
    `(let (,(car bindings)) (let* ,(cdr bindings) ,expr))
  )
)

;;; Just For Fun Problems


; Helper Functions for you
(define (cadr lst) (car (cdr lst)))
(define (cddr lst) (cdr (cdr lst)))
(define (caddr lst) (car (cdr (cdr lst))))
(define (cdddr lst) (cdr (cdr (cdr lst))))

(define-macro (infix expr)
  (define (contains sym lst)
    (cond ((null? lst) #f)
          ((eq? (car lst) sym) #t)
          (else (contains sym (cdr lst)))))
  (define (split-at sym lst)
    (define (helper pre post)
      (cond ((null? post) #f)
            ((eq? (car post) sym) (cons pre (cdr post)))
            (else (helper (append pre (list (car post))) (cdr post)))))
    (helper '() lst))
  (cond
    ((not (list? expr)) expr)
    ((null? (cdr expr)) `(infix ,(car expr)))
    ((contains '+ expr)
     (let ((parts (split-at '+ expr)))
       `(+ (infix ,(car parts)) (infix ,(cdr parts)))))
    ((contains '* expr)
     (let ((parts (split-at '* expr)))
       `(* (infix ,(car parts)) (infix ,(cdr parts)))))
    (else (car expr))))


; only testing if your code could expand to a valid expression 
; resulting in my/and/2 and my/or/2 not hygienic
(define (gen-sym) 'sdaf-123jasf/a123)

; in these two functions you can use gen-sym function.
; assumption:
; 1. scm> (eq? (gen-sym) (gen-sym))
;    #f
; 2. all symbol generate by (gen-sym) will not in the source code before macro expansion
(define-macro (my/and/2 operands)
  'YOUR-CODE-HERE
)

(define-macro (my/or/2 operands)
  'YOUR-CODE-HERE
)
